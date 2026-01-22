from django.contrib.auth import get_user_model
from django import forms
from django.forms import inlineformset_factory
from .models import Product,Category, Images

class ProductForm(forms.ModelForm):
    """
    Form for admin to add new products to the site
    """
    class Meta:
        model = Product
        fields = ['name','description','price','main_category','sub_category','stock_level','delivery_cost','promoted',]
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
            'price': forms.NumberInput(attrs={'step':'0.01'}),
        }
class ImageForm(forms.ModelForm):
    """
    Form for admin to upload an image to be
    used by formset
    """
    class Meta:
        model = Images
        fields = ['image','position','primary_image',]
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'position': forms.NumberInput(attrs={'min': 0}),
        }
    

ImageFormSet = inlineformset_factory(
    Product,
    Images, 
    form=ImageForm,
    extra=3,
    can_delete=True,
    max_num=8,
    validate_max=True,
    )

    # name = 
    # description = 
    # price = 
    # main_category =
    # sub_category = 
    # stock_level = 
    # delivery_cost = 
    # promoted =