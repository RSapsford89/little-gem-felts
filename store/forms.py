from django import forms
from django.forms import inlineformset_factory
from .models import Product, Images


class ProductForm(forms.ModelForm):
    """
    Form for admin to add new products to the site
    """
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'main_category',
            'sub_category',
            'stock_level',
            'delivery_cost',
            'promoted',]
        labels = {
            'name': 'Product Title',
            'description': 'Product Description',
            'price': 'Price (£)',
            'main_category': 'Category',
            'sub_category': 'Sub-Category',
            'stock_level': 'Units in Stock',
            'delivery_cost': 'Shipping Cost (£)',
            'promoted': 'Promote on Homepage?',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ImageForm(forms.ModelForm):
    """
    Form for admin to upload an image to be
    used by formset
    """
    class Meta:
        model = Images
        fields = ['image', 'position', 'primary_image',]
        labels = {
            'image': 'Upload Image',
            'position': 'Display Order (1 = First)',
            'primary_image': 'Set as Main Product Image',
        }
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'position': forms.NumberInput(attrs={'min': 0}),
        }


ImageFormSet = inlineformset_factory(
    Product,
    Images,
    form=ImageForm,
    extra=1,
    can_delete=True,
    max_num=8,
    validate_max=True,
    )
