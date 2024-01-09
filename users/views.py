# users/views.py

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import CustomUserCreationForm, CustomPasswordResetForm, UserProfileForm, SubscriptionForm, CustomLoginForm
from .models import CustomUser
from .tokens import account_activation_token


@login_required
def account_activation_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш адрес электронной почты успешно подтвержден.')
    else:
        messages.error(request, 'Неверная ссылка для подтверждения.')

    return redirect('catalog:home')  # Измените на URL, на который вы хотите перенаправить после подтверждения


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Пожалуйста, проверьте ваш логин и пароль.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class CustomRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:registration_success')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Подтверждение регистрации'
        message = render_to_string('users/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

        messages.success(self.request, 'Пожалуйста, проверьте вашу почту и подтвердите регистрацию.')

        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'users/update_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('catalog:home')


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
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
