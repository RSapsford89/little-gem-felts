from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from store.models import Product
from order.models import Order, OrderLineItem
from .forms import ShippingForm
from basket.contexts import basket_contents
from django.views.decorators.csrf import csrf_exempt
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def order_confirmation(request):
    """
    display an order confirmation page after the
    order has been successfully created
    """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'order/order_confirmation.html', context)


def payment(request):
    """Handle the payment page with Stripe Payment Element"""
    client_secret = request.session.get('client_secret')
    order_id = request.session.get('order_id')

    if not client_secret or not order_id:
        messages.error(request, "No payment information found")
        return redirect('basket:view_basket')

    order = get_object_or_404(Order, order_id=order_id)

    context = {
        'order': order,
        'client_secret': client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'order/payment.html', context)


def create_order(request):
    basket = request.session.get('basket', {})
    # check for empty basket and if it is GET or POST method
    # to determine proper response
    if not basket:
        if request.method == 'POST':
            return JsonResponse({'success': False, 'error': 'Basket is empty'}, status=400)
        else:
            messages.error(request, "Your basket is empty at the moment.")
            return redirect('store:store')
        
    if request.method == 'POST':
        form = ShippingForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            pid = request.session.get('id')
            order.stripe_pid = pid

            if pid:
                repeat_order = Order.objects.filter(stripe_pid=pid, is_paid=False).first()
                if repeat_order:
                    # use the clean_up def to remove
                    repeat_order.clean_up()
                    repeat_order.delete()

            if request.user.is_authenticated:
                user = request.user
                order.user = user

            order.save()

            try:
                for product_id, quantity in basket.items():
                    product = get_object_or_404(Product, pk=product_id)

                    if quantity <= product.stock_level:
                        # reduce stock qty
                        product.stock_level -= quantity
                        product.save()

                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            product_price=product.price,
                            product_delivery=product.delivery_cost,
                            quantity=quantity,
                        )
                    else:
                        order.delete()
                        return JsonResponse({'success': False, 'error': f'{product.name} does not have enough stock'}, status=400)
            except Exception as e:
                # adjust stock to previous level before finishing
                order.clean_up()

                return JsonResponse({'success': False, 'error': f'Error creating order: {e}'}, status=400)

            if pid:
                try:
                    stripe.PaymentIntent.modify(
                        pid,
                        receipt_email=order.email,
                        metadata={
                            'order_id': str(order.order_id)
                        }
                    )
                except Exception as e:
                    print(f'error with pid {e}')
                    return JsonResponse({'success': False, 'error': 'Payment processing error'}, status=400)

            request.session['order_id'] = str(order.order_id)

            messages.success(request, 'order created')
            return JsonResponse({'success': True, 'message': f'Order created{str(order)}'})
        else:
            return JsonResponse({'success': False, 'error': form.errors}, status=400)

    else:  # For GET requests, render the form as usual
        basket_context = basket_contents(request)
        grand_total = basket_context['grand_total']

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(grand_total * 100),
                currency='gbp',
                automatic_payment_methods={'enabled': True},
            )
            request.session['client_secret'] = intent.client_secret
            request.session['id'] = intent.id
        except Exception as e:

            messages.error(request, f"Stripe error: {e}")
            return redirect('basket:view_basket')

        if request.user.is_authenticated:
            user = request.user
            prefill_data = {
                'full_name': user.profile.ship_name,
                'email': user.email,
                'phoneNumber': user.profile.phoneNumber,
                'street_address1': user.profile.street_address1,
                'street_address2': user.profile.street_address2,
                'town_city': user.profile.town_city,
                'postcode': user.profile.postcode,
                'country': user.profile.country,
            }
            form = ShippingForm(initial=prefill_data)
        else:
            form = ShippingForm()

    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'order/create_order.html', context)
