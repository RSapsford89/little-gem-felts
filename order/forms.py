from django.contrib.auth import get_user_model
from django import forms
from store.models import Product, Category
from .models import Order


class ShippingForm(forms.ModelForm):
    """
    Form for gathering the user's shipping details
    """
    class Meta:
        model = Order
        fields = [
                'full_name',
                'email',
                'phoneNumber',
                'street_address1',
                'street_address2',
                'town_city',
                'postcode',
                'country',
                ]