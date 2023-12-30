from typing import Dict, Union

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
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
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
    success_url = reverse_lazy("success-register")
    redirect_authenticated_user = True

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponseRedirect:
        user = form.save()

        domain: str = get_current_site(self.request).domain
        uidb64: str = urlsafe_base64_encode(force_bytes(user.pk))
        token: str = account_activation_token.make_token(user)
        from_email: str = settings.COMPANY_EMAIL

        subject = "Account Activation"
        message: str = render_to_string(
            "emails/account_activation_email.html",
            {"user": user, "domain": domain, "uidb64": uidb64, "token": token},
        )

        user.email_user(subject=subject, message=message, from_email=from_email)

        return super().form_valid(form)


class SuccessRegisterView(TemplateView):
    template_name = "users/register_success.html"


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_invalid(self, form: CustomAuthenticationForm) -> HttpResponse:
        response: HttpResponse = super().form_invalid(form)
        username: str = form.cleaned_data.get("username")
        try:
            user: User = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "User does not exist. Please check your email and password.",
            )
        else:
            if not user.is_active:
                messages.warning(
                    self.request,
                    "User is not active. Please check your email and active your account.",
                )
            else:
                messages.warning(self.request, message="Incorrect password!")
        return response


class ActivateAccountView(TemplateView):
    template_name = "users/activation_result.html"

    def get_context_data(self, **kwargs) -> Dict[str, str]:
        context: Dict = super().get_context_data(**kwargs)
        uidb64: str = self.kwargs.get("uidb64")
        token: str = self.kwargs.get("token")
        information = "failed"

        try:
            uid: str = force_str(urlsafe_base64_decode(uidb64))
            user: Union[User | None] = User.objects.get(pk=uid)
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
    success_url = reverse_lazy("forgot-password-done")
    template_name = "users/forgot_password.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/forgot_password_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("forgot-password-complete")
    template_name = "users/forgot_password_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/forgot_password_complete.html"


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
