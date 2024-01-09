# users/urls.py

from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    CustomRegistrationView, CustomLoginView, CustomLogoutView,
    CustomPasswordResetView, UserProfileView, UserSubscriptionsView, account_activation_view
)

app_name = 'users'

urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('forgot-password/', CustomPasswordResetView.as_view(), name='forgot_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('subscriptions/', UserSubscriptionsView.as_view(), name='subscriptions'),
    path('activate/<uidb64>/<token>/', account_activation_view, name='account_activation'),
]
