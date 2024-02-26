from celery import shared_task
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


@shared_task
def send_activation_email(
    user_id: int, subject: str, message: str, from_email: str
) -> None:
    user = get_object_or_404(User, pk=user_id)
    user.email_user(subject=subject, message=message, from_email=from_email)
