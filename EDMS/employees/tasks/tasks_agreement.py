from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from employees.models.models_agreement import Agreement


@shared_task
def set_agreement_is_current() -> None:
    set_agreement_is_current_for_starting_agreement()
    set_agreement_is_current_for_ending_agreement()


def set_agreement_is_current_for_ending_agreement() -> None:
    for agreement in Agreement.objects.filter(end_date_actual=timezone.now().date() - timezone.timedelta(days=1)):
        agreement.is_current = False
        agreement.save()


def set_agreement_is_current_for_starting_agreement() -> None:
    for agreement in Agreement.objects.filter(start_date=timezone.now().date()):
        agreement.is_current = True
        agreement.save()


@shared_task
def remind_expiring_agreement(remind_days: int):
    for agreement in Agreement.objects.filter(end_date=timezone.now().date() + timezone.timedelta(days=remind_days)):
        send_mail_to_user(agreement)


def send_mail_to_user(agreement: Agreement) -> None:
    subject_to_leave_user = "Expiring agreement!"
    message_to_leave_user = render_to_string(
        template_name="email_templates/expiring_agreement_email.html",
        context={
            "agreement": agreement,
        },
    )
    agreement.user.email_user(
        subject=subject_to_leave_user,
        message=message_to_leave_user,
        from_email=settings.EMAIL_HOST_USER,
    )
