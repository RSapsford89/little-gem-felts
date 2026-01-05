from django.urls import path
from .import views

app_name = 'basket'

urlpatterns = [
    path('basket/', views.view_bag, name='view_bag'),
    path('add/<id>/', views.add_to_bag, name='add_to_bag'),
    path('update/<id>/', views.update_bag, name='update_bag'),
    path('remove/<id>/', views.remove_from_bag, name='remove_from_bag'),
]