from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import userProfile, Testimonial

User = get_user_model()
# This code is based largely on the custom form built in
# the YouTube video by Codemy.com: https://www.youtube.com/watch?v=HdrOcreAXKk&t=397s
# Form taken from Collaborative Calendar P3 project and
# updated for this project

class CustomSignupForm(SignupForm):
    """
    extend the allauth signup form to include
    the name fields
    """
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')


    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CustomUserForm(UserCreationForm):
    """
    UserCreationForm is bound to the AUTH_USER_MODEL string
    This stops the form Meta.model from using default auth.User
    instead of this one
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


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
        fields = ['phoneNumber', 'ship_name', 'street_address1', 'street_address2', 'town_city', 'postcode', 'country', 'profile_pic']
        widgets = {
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'ship_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address1': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address2': forms.TextInput(attrs={'class': 'form-control'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }


class TestimonialForm(forms.ModelForm):
    """
    Form for submitting testimonials
    """
    class Meta:
        model = Testimonial
        fields = ['rating', 'short_review', 'long_review']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'short_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'long_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
