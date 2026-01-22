from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    
    path('<int:product_id>/', views.create_order, name='create_order'),
]