from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import userProfile

User = get_user_model()
# This code is based largely on the custom form built in
# the YouTube video by Codemy.com: https://www.youtube.com/watch?v=HdrOcreAXKk&t=397s
# Form taken from Collaborative Calendar P3 project and
# updated for this project


class CustomUserForm(UserCreationForm):
    """
    UserCreationForm is bound to the AUTH_USER_MODEL string
    This stops the form Meta.model from using default auth.User
    instead of this one
    """
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfilePictureForm(forms.ModelForm):
    """
    Form for uploading/changing profile picture
    """
    class Meta:
        model = userProfile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile information
    """
    class Meta:
        model = userProfile
        fields = ['phoneNumber', 'ship_name', 'street_address1', 'street_address2', 'town_city', 'postcode', 'profile_pic']
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address1': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address2': forms.TextInput(attrs={'class': 'form-control'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
