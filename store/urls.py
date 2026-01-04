from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name='store'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]