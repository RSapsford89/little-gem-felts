from django.urls import path
from .import views

app_name = 'basket'

urlpatterns = [
    path('basket/', views.view_basket, name='view_basket'),
    path('add/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('update/<int:product_id>/', views.update_basket, name='update_basket'),
    path('remove/<int:product_id>/', views.remove_basket, name='remove_basket'),
]