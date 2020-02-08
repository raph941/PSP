import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserProfile
from cloudinary.forms import CloudinaryFileField


MALE = 'Male'
FEMALE = 'Female'
GENDER = [
    (MALE, 'male'),
    (FEMALE, 'female'),
]


class RegularUserCreationForm(UserCreationForm):
    first_name = forms.CharField( max_length=30, required=False)
    last_name = forms.CharField( max_length=30, required=False)
    date_of_birth = forms.DateField()
    email = forms.EmailField(max_length = 254, required=False, help_text='enter a valid email address.')
    phone_number = forms.CharField( max_length=30, required=False)
    nationality = forms.CharField( max_length=30, required=False)
    profile_pic = CloudinaryFileField(
        options = {
            'crop': 'thumb',
            'width': 420,
            'height': 400,
            'folder': 'Regular profile_pic'
       }
    )
    bio = forms.CharField( max_length=2555, required=False)

    class Meta:
        model = User
        User.is_regular = True
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'bio', 'email', 
            'phone_number', 'nationality', 'profile_pic', 'password1', 'password2')



class AdminUserCreationForm(UserCreationForm):
    first_name = forms.CharField( max_length=30, required=False)
    last_name = forms.CharField( max_length=30, required=False)
    date_of_birth = forms.DateField()
    email = forms.EmailField(max_length = 254, required=False, help_text='enter a valid email address.')
    phone_number = forms.CharField( max_length=30, required=False)
    nationality = forms.CharField( max_length=30, required=False)
    profile_pic = CloudinaryFileField(
        options = {
            'crop': 'thumb',
            'width': 420,
            'height': 400,
            'folder': 'Admin profile_pic'
       }
    )

    class Meta:
        model = User
        User.is_admin = True
        User.is_regular = False
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'email', 
            'phone_number', 'nationality', 'profile_pic', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'nationality', 'profile_pic', 'bio')