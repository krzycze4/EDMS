from typing import Dict, Union

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, TemplateView
from users.forms import CustomUserCreationForm
from users.models import User
from users.tokens import account_activation_token


class UserRegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "users/register/register.html"
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
    template_name = "users/register/register_success.html"


class ActivateAccountView(TemplateView):
    template_name = "users/register/activation_result.html"

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
