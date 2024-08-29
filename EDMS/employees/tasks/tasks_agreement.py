from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from employees.models.models_agreement import Agreement


@shared_task
def set_agreement_is_current() -> None:
    """
    Sets the 'is_current' status of agreements based on their start and end dates.

    This function updates the status of agreements that are starting today
    or ended yesterday by calling helper functions.
    """
    set_agreement_is_current_for_starting_agreement()
    set_agreement_is_current_for_ending_agreement()


def set_agreement_is_current_for_ending_agreement() -> None:
    """
    Sets 'is_current' to False for agreements that ended yesterday.

    This function finds all agreements that ended yesterday
    and marks them as no longer current.
    """
    for agreement in Agreement.objects.filter(end_date_actual=timezone.now().date() - timezone.timedelta(days=1)):
        agreement.is_current = False
        agreement.save()


def set_agreement_is_current_for_starting_agreement() -> None:
    """
    Sets 'is_current' to True for agreements that start today.

    This function finds all agreements that start today
    and marks them as current.
    """
    for agreement in Agreement.objects.filter(start_date=timezone.now().date()):
        agreement.is_current = True
        agreement.save()


@shared_task
def remind_expiring_agreement(remind_days: int):
    """
    Sends reminder emails to users with agreements that will expire soon.

    Args:
        remind_days (int): Number of days before the expiration to send the reminder.

    This function finds agreements that will expire in the specified number
    of days and sends a reminder email to the associated user.
    """
    for agreement in Agreement.objects.filter(end_date=timezone.now().date() + timezone.timedelta(days=remind_days)):
        send_mail_to_user(agreement)


def send_mail_to_user(agreement: Agreement) -> None:
    """
    Sends an email notification to the user about an expiring agreement.

    Args:
        agreement (Agreement): The agreement that is about to expire.

    This function composes and sends an email to the user
    associated with the given agreement, notifying them that it is expiring soon.
    """
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
