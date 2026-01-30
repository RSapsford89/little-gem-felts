
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from order.models import Order


import stripe

class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(content=f'Unhandled event type {event["type"]}', status=200)
        

    def handle_payment_intent_succeeded(self, event):
        # get the order ID, PID, update order with the PID and paid to True
        intent = event.data.object
        metadata = intent.get('metadata',{})
        order_id = metadata.get('order_id')
        if not order_id:
            # no order id sent in metadata
            print("no order_id")
            return HttpResponse(content="PaymentIntent succeeded but no order_id in metadata")
        
        try:
            order = Order.objects.get(order_id=order_id)
            order.stripe_pid = intent.id
            order.is_paid = True
            order.save()
            print(order.is_paid)
            print(order.order_id)
            return HttpResponse(content='PaymentIntent was successful!', status=200)
        
        except Order.DoesNotExist:
            return HttpResponse(content="order not found",status=400)
        except Exception as e:
            return HttpResponse(content=f"unable to update order: {e}", status=500)


    def handle_payment_intent_failed(self, event):
        # get the order ID, PID, update order with the PID and paid to True
        intent = event.data.object
        metadata = intent.get('metadata',{})
        order_id = metadata.get('order_id')
        if not order_id:
            # no order id sent in metadata
            return HttpResponse(content="PaymentIntent failed - no order_id in metadata")

        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()            

            return HttpResponse(content=f'PaymentIntent was failed! Removed Order {order_id}', status=200)

        except Order.DoesNotExist:
            return HttpResponse(content="order not found",status=400)
        except Exception as e:
            return HttpResponse(content=f"unable to update order: {e}", status=500)

# Code from Boutique Ado and Stripe QuickStart docs
@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    except Exception as e:
        return HttpResponse(content=e, status=400)
    
    # set up a webhook handler
    handler = StripeWH_Handler(request)

    # map the webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_failed,
        
    }

    # get webhook type from Stripe
    event_type = event['type']

    print("stripe event:", event_type)
    # if there's a handler for it, get it from the event map
    # use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # call the event handler with the event
    response = event_handler(event)
    return response