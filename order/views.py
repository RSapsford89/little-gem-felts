from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from store.models import Product
from order.models import Order, OrderLineItem
from .forms import ShippingForm
from basket.contexts import basket_contents
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_order(request):
    """
    Take context basket, shipping form,
    contact form or user details, stripe pid
    to create an 'order' object
    """
    if request.method == 'POST':
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request,'Your basket is empty')
            return redirect('basket:view_basket')
        try:
            form = ShippingForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                try:
                    for product_id, quantity in basket.items():
                        product = get_object_or_404(Product, pk=product_id)
                        if quantity <= product.stock_level:
                            OrderLineItem.objects.create(
                                order = order,
                                product = product,
                                product_name = product.name,
                                product_price = product.price,
                                product_delivery = product.delivery_cost,
                                quantity = quantity,
                            )                            
                        else:
                            order.delete()
                            messages.error(request, f'{product.name} does not have enough stock available')
                            return redirect('basket:view_basket')
                            # delete order
                    order.update_total()
                    
                
                    messages.success(request, f'Order {order.order_id} has been created')
                    # Clear the basket after successful order
                    request.session['basket'] = {}
                    request.session['order_id'] = str(order.order_id)
                    return redirect('order:order_confirmation')

                except (Exception, ValueError) as error:
                    messages.error(request, 'Failed to check basket item against stock')
                    order.delete()
                    return redirect('basket:view_basket')
        except Exception as error:
            messages.error(request,f'Shipping form not valid: {error}')
            return redirect('basket:view_basket')
    else:
        # GET request - initialize empty form (runs on page load/1st)
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, 'Your basket is empty')
            return redirect('basket:view_basket')
        
        #get basket total from context processor
        basket_context = basket_contents(request)
        grand_total = basket_context['grand_total']
        # create the STRIPE payment intent after order created and 
        # we know what the total to charge is. From Stripe Docs
        intent = stripe.PaymentIntent.create(
            amount= int(grand_total)*100, # values in pence
            currency= 'gbp',
            automatic_payment_methods={
                'enabled': True,
            },
           # metadata={'order_id': str(order.order_id)}  # Add order reference in metadata
        )
        
        # Store client_secret in the session for the payment page to use
        request.session['client_secret'] = intent.client_secret
        
        # Store order_id in session
        #request.session['order_id'] = str(order.order_id)
        
        # Redirect to a payment page that will use the client secret
        # return redirect('order:payment')
        
        if request.user.is_authenticated:
            user = request.user
            prefill_data ={
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
            messages.success(request,"User's saved detail loaded")
        else:
            form = ShippingForm()
        # Debug: Check if keys are loaded
        if not settings.STRIPE_PUBLIC_KEY:
            messages.warning(request, 'Stripe public key is missing.')
    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'order/create_order.html', context)

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
    return render(request,'order/order_confirmation.html', context)

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