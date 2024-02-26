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
def set_agreement_is_current() -> None:
    set_agreement_is_current_for_starting_agreement()
    set_agreement_is_current_for_ending_agreement()


def set_agreement_is_current_for_ending_agreement() -> None:
    for agreement in Agreement.objects.filter(
        end_date_actual=timezone.now().date() - timezone.timedelta(days=1)
    ):
        agreement.is_current = False
        agreement.save()


def set_agreement_is_current_for_starting_agreement() -> None:
    for agreement in Agreement.objects.filter(start_date=timezone.now().date()):
        agreement.is_current = True
        agreement.save()


@shared_task
def set_user_is_active_to_false() -> None:
    for user in User.objects.filter(is_superuser=False):
        if not user.agreements.filter(is_current=True).exists():
            user.is_active = False
            user.save()


@shared_task
def set_user_vacation_left() -> None:
    for user in User.objects.filter(is_superuser=False, is_active=True):
        current_employment_agreement = user.agreements.filter(
            type=Agreement.EMPLOYMENT, is_current=True
        )
        if current_employment_agreement:
            add_new_vacation_days(
                user=user, current_employment_agreement=current_employment_agreement
            )


def add_new_vacation_days(user: User, current_employment_agreement: Agreement) -> None:
    user.vacation_left += count_granted_vacation_from_agreement(
        current_employment_agreement=current_employment_agreement, user=user
    )
    user.save()


def count_granted_vacation_from_agreement(
    current_employment_agreement: Agreement, user: User
) -> int:
    months_in_year = 12
    work_months_current_year = count_work_months_current_year(
        start_date=current_employment_agreement.start_date,
        end_date_actual=current_employment_agreement.end_date_actual,
    )
    vacation_from_agreement = ceil(
        work_months_current_year * user.vacation_days_per_year / months_in_year
    )
    return vacation_from_agreement


def count_work_months_current_year(start_date: date, end_date_actual: date) -> int:
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
    for vacation in Vacation.objects.filter(
        start_date=timezone.now().date() + timezone.timedelta(days=remind_days)
    ):
        send_mail_to_leave_user(vacation)
        send_mails_to_substitute_users(vacation)


def send_mails_to_substitute_users(vacation: Vacation) -> None:
    subject_to_substitute_user = "Your co-worker is going to holidays."
    for substitute_user in vacation.substitute_users.all():
        message_to_substitute_user = render_to_string(
            template_name="emails/substitute_user_email.html",
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
            from_email=settings.COMPANY_EMAIL,
        )


def send_mail_to_leave_user(vacation: Vacation) -> None:
    subject_to_leave_user = "Holidays!"
    message_to_leave_user = render_to_string(
        template_name="emails/leave_user_email.html",
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
        from_email=settings.COMPANY_EMAIL,
    )


@shared_task
def remind_expiring_agreement(remind_days: int):
    for agreement in Agreement.objects.filter(
        end_date=timezone.now().date() + timezone.timedelta(days=remind_days)
    ):
        send_mail_to_user(agreement)


def send_mail_to_user(agreement: Agreement) -> None:
    subject_to_leave_user = "Expiring agreement!"
    message_to_leave_user = render_to_string(
        template_name="emails/expiring_agreement_email.html",
        context={
            "agreement": agreement,
        },
    )
    agreement.user.email_user(
        subject=subject_to_leave_user,
        message=message_to_leave_user,
        from_email=settings.COMPANY_EMAIL,
    )
