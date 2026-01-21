from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('products/', views.product_management, name='product_management'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
]
