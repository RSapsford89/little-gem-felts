from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('products/', views.product_management, name='product_management'),
]
