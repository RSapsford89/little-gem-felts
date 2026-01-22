from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('products/', views.product_management, name='product_management'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('blog/', views.blog_management, name='blog_management'),
    path('blog/add/', views.add_post, name='add_post'),
    path('blog/edit/<int:post_id>/', views.edit_post, name='edit_post'),
]
