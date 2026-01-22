from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from store.models import Product
from userprofile.models import userProfile

# Create your views here.

def create_order(request):
    """
    Take context basket, shipping form,
    contact form or user details, stripe pid
    to create an 'order' object
    """
    if request.method == 'POST':
        try:
            basket = request.session.get('basket', {})
            
        except Exception as error:
            return error