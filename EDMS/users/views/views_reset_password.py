from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from users.forms import CustomPasswordResetForm, CustomSetPasswordForm


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
