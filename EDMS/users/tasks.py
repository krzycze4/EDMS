from typing import Any, Dict

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import get_object_or_404

User = get_user_model()


@shared_task
def send_activation_email(user_id: int, subject: str, message: str, from_email: str) -> None:
    """
    Send an activation email to a user.

    Args:
        user_id (int): The ID of the user to send the email to.
        subject (str): The subject of the email.
        message (str): The content of the email.
        from_email (str): The email address of the sender.

    Returns:
        None
    """
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
    """
    Send a password reset email.

    Args:
        subject_template_name (str): The name of the template for the email subject.
        email_template_name (str): The name of the template for the email body.
        context (Dict[str, Any]): Data to use in the email templates.
        from_email (str): The email address of the sender.
        to_email (str): The email address of the recipient.
        html_email_template_name (str): The name of the template for the HTML email body.

    Returns:
        None
    """
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


@shared_task
def set_user_is_active_to_false() -> None:
    """
    Set inactive status for users who do not have current agreements.

    Args:
        None

    Returns:
        None
    """
    for user in User.objects.filter(is_superuser=False):
        if not user.agreements.filter(is_current=True).exists():
            user.is_active = False
            user.save()
