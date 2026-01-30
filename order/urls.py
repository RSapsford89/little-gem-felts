from django.urls import path
from . import views
from . import stripe_webhook
app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    path('webhook/', stripe_webhook.webhook, name='stripe_webhook')
    # path('order/shipping-form/', views.shippingForm, name='shipping_form_ajax'),
]
