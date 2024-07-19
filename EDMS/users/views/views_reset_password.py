from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from users.forms.forms_password import CustomPasswordResetForm, CustomSetPasswordForm


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "email_templates/forgot_password_email.html"
    form_class = CustomPasswordResetForm
    from_email = settings.EMAIL_HOST_USER
    subject_template_name = "email_templates/email_subject.txt"
    success_url = reverse_lazy("forgot-password-done")
    template_name = "users/forgot_password/forgot_password.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/forgot_password/forgot_password_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("forgot-password-complete")
    template_name = "users/forgot_password/forgot_password_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/forgot_password/forgot_password_complete.html"
