# users/urls.py

from django.urls import path
from .views import (
    CustomRegistrationView, CustomLoginView, CustomLogoutView,
    CustomPasswordResetView, UserProfileView, UserSubscriptionsView
)

app_name = 'users'

urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('forgot-password/', CustomPasswordResetView.as_view(), name='forgot_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('subscriptions/', UserSubscriptionsView.as_view(), name='subscriptions'),
]
