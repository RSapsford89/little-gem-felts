from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
]