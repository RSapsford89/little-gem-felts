from django.contrib.auth import get_user_model
from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','description','price','main_category','sub_category','stock_level','delivery_cost','promoted',]
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
            'price': forms.NumberInput(attrs={'step':'0.01'}),
        }
    
    
    # name = 
    # description = 
    # price = 
    # main_category =
    # sub_category = 
    # stock_level = 
    # delivery_cost = 
    # promoted =