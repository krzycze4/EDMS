from datetime import date
from math import ceil

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils import timezone
from employees.models.models_agreement import Agreement
from employees.models.models_vacation import Vacation

User = get_user_model()


@shared_task
def set_user_vacation_left() -> None:
    """
    Updates the remaining vacation days for each active user.

    The function finds the current employment agreement for each user
    and adds the new vacation days to the user's balance.
    """
    for user in User.objects.filter(is_superuser=False, is_active=True):
        try:
            current_employment_agreement = user.agreements.get(type=Agreement.EMPLOYMENT, is_current=True)
        except Agreement.DoesNotExist:
            continue
        add_new_vacation_days(user=user, current_employment_agreement=current_employment_agreement)


def add_new_vacation_days(user: User, current_employment_agreement: Agreement) -> None:
    """
    Adds new vacation days to the user's remaining vacation days.

    Args:
        user (User): The user whose vacation days are being updated.
        current_employment_agreement (Agreement): The user's current employment agreement.
    """
    user.vacation_left += count_granted_vacation_from_agreement(
        current_employment_agreement=current_employment_agreement, user=user
    )
    user.save()


def count_granted_vacation_from_agreement(current_employment_agreement: Agreement, user: User) -> int:
    """
    Calculates the number of vacation days granted based on the employment agreement.

    Args:
        current_employment_agreement (Agreement): The user's current employment agreement.
        user (User): The user for whom the vacation days are being calculated.

    Returns:
        int: The number of vacation days granted this year.
    """
    months_in_year = 12
    work_months_current_year = count_work_months_current_year(
        start_date=current_employment_agreement.start_date,
        end_date_actual=current_employment_agreement.end_date_actual,
    )
    vacation_from_agreement = ceil(work_months_current_year * user.vacation_days_per_year / months_in_year)
    return vacation_from_agreement


def count_work_months_current_year(start_date: date, end_date_actual: date) -> int:
    """
    Counts the number of months worked by the user in the current year.

    Args:
        start_date (date): The start date of the employment agreement.
        end_date_actual (date): The actual end date of the employment agreement.

    Returns:
        int: The number of months worked in the current year.
    """
    start_month = start_date.month
    end_month = end_date_actual.month
    if start_date.year < timezone.now().year:
        january = 1
        start_month = january
    if end_date_actual.year > timezone.now().year:
        december = 12
        end_month = december
    return end_month - start_month + 1


@shared_task
def remind_vacations(remind_days: int) -> None:
    """
    Sends email reminders about upcoming vacations to users.

    Args:
        remind_days (int): The number of days before the vacation start date to send the reminder.
    """
    for vacation in Vacation.objects.filter(start_date=timezone.now().date() + timezone.timedelta(days=remind_days)):
        send_mail_to_leave_user(vacation)
        send_mails_to_substitute_users(vacation)


def send_mails_to_substitute_users(vacation: Vacation) -> None:
    """
    Sends an email to users who will be substitutes during the vacation.

    Args:
        vacation (Vacation): The vacation object containing details about the leave.
    """
    subject_to_substitute_user = "Your co-worker is going to holidays."
    for substitute_user in vacation.substitute_users.all():
        message_to_substitute_user = render_to_string(
            template_name="email_templates/substitute_user_email.html",
            context={
                "substitute_user": substitute_user,
                "leave_user": vacation.leave_user,
                "start_date": vacation.start_date,
                "end_date": vacation.start_date,
            },
        )
        substitute_user.email_user(
            subject=subject_to_substitute_user,
            message=message_to_substitute_user,
            from_email=settings.EMAIL_HOST_USER,
        )


def send_mail_to_leave_user(vacation: Vacation) -> None:
    """
    Sends an email to the user who is going on vacation.

    Args:
        vacation (Vacation): The vacation object containing details about the leave.
    """
    subject_to_leave_user = "Holidays!"
    message_to_leave_user = render_to_string(
        template_name="email_templates/leave_user_email.html",
        context={
            "leave_user": vacation.leave_user,
            "vacation_start_date": vacation.start_date,
            "vacation_end_date": vacation.end_date,
            "substitute_users": vacation.substitute_users.all(),
        },
    )
    vacation.leave_user.email_user(
        subject=subject_to_leave_user,
        message=message_to_leave_user,
        from_email=settings.EMAIL_HOST_USER,
    )
