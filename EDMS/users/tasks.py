from typing import Any, Dict

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import get_object_or_404

User = get_user_model()


@shared_task
def send_activation_email(
    user_id: int, subject: str, message: str, from_email: str
) -> None:
    user = get_object_or_404(User, pk=user_id)
    user.email_user(subject=subject, message=message, from_email=from_email)


@shared_task
def send_mail_reset_password(
    subject_template_name: str,
    email_template_name: str,
    context: Dict[str, Any],
    from_email: str,
    to_email: str,
    html_email_template_name: str,
):
    context["user"] = User.objects.get(pk=context["user"])
    PasswordResetForm.send_mail(
        None,
        subject_template_name=subject_template_name,
        email_template_name=email_template_name,
        context=context,
        from_email=from_email,
        to_email=to_email,
        html_email_template_name=html_email_template_name,
    )
