from django.urls import path
from .import views

app_name = 'basket'

urlpatterns = [
    path('basket/', views.view_basket, name='view_basket'),
    path('add/<id>/', views.add_to_basket, name='add_to_basket'),
    path('update/<id>/', views.update_basket, name='update_basket'),
    path('remove/<id>/', views.remove_basket, name='remove_basket'),
]