from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm
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

        subject = "Account Activation"
        message = render_to_string(
            "users/account_activation_email.html",
            {"user": user, "domain": domain, "uidb64": uidb64, "token": token},
        )

        user.email_user(subject=subject, message=message, from_email="EDMS@test.com")

        return super().form_valid(form)


class SuccessRegisterView(TemplateView):
    template_name = "users/register_success.html"


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("dashboard")
    form_class = CustomAuthenticationForm


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
