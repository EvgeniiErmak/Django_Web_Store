# users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
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
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'phone_number', 'country']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number', 'country']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'description']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
