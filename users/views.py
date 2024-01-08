# users/views.py
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomPasswordResetForm, UserProfileForm, SubscriptionForm
from .models import CustomUser

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

class CustomRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')

class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'users/update_profile.html'
    form_class = UserProfileForm  # Поменяйте на соответствующую форму, если есть
    success_url = reverse_lazy('catalog:home')

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm  # Поменяйте на соответствующую форму, если есть
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = self.request.user.profile.subscriptions.all()
        return context

class UserSubscriptionsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        subscriptions = user.subscriptions.all()
        subscription_form = SubscriptionForm()
        context['subscriptions'] = subscriptions
        context['subscription_form'] = subscription_form
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            subscription = subscription_form.save(commit=False)
            subscription.user = user
            subscription.save()
            return redirect('users:subscriptions')
        return render(request, self.template_name, {'subscription_form': subscription_form})
