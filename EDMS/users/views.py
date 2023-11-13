from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomUserCreationForm,
)
from .models import User
from .tokens import account_activation_token


class UserRegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("success_register")

    def form_valid(self, form):
        user = form.save()

        domain = get_current_site(self.request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        from_email = settings.COMPANY_EMAIL

        subject = "Account Activation"
        message = render_to_string(
            "emails/account_activation_email.html",
            {"user": user, "domain": domain, "uidb64": uidb64, "token": token},
        )

        user.email_user(subject=subject, message=message, from_email=from_email)

        return super().form_valid(form)


class SuccessRegisterView(TemplateView):
    template_name = "users/register_success.html"


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("dashboard")
    form_class = CustomAuthenticationForm

    def form_invalid(self, form):
        response = super().form_invalid(form)
        username = form.cleaned_data.get("username")
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "User does not exist. Please check your email and password.",
            )
        else:
            if not user.is_active:
                messages.error(
                    self.request,
                    "User is not active. Please check your email and active your account.",
                )
        return response


class ActivateAccountView(TemplateView):
    template_name = "users/activation_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb64 = self.kwargs.get("uidb64")
        token = self.kwargs.get("token")
        information = "failed"

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            information = "successfully"

        context["information"] = information
        return context


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "emails/forgot_password_email.html"
    form_class = CustomPasswordResetForm
    from_email = settings.COMPANY_EMAIL
    subject_template_name = "emails/email_subject.txt"
    success_url = reverse_lazy("forgot_password_done")
    template_name = "users/forgot_password.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/forgot_password_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("forgot_password_complete")
    template_name = "users/forgot_password_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/forgot_password_complete.html"


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
