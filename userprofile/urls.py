from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.profile_view, name='profile_view'),
    # path('edit-picture/', views.edit_profile_picture, name='edit_profile_picture'),
    path('edit/', views.edit_view, name='edit_view'),
]