# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, User
from .models import CustomUser, Profile, Subscription


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country']


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = CustomUser
        fields = ['email']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number', 'country']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'description']
