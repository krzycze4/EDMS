from datetime import date
from math import ceil

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from employees.models.models_agreement import Agreement

User = get_user_model()


@shared_task
def set_agreement_is_current():
    for agreement in Agreement.objects.filter(start_date=timezone.now().date()):
        agreement.is_current = True
        agreement.save()

    for agreement in Agreement.objects.filter(
        end_date_actual=timezone.now().date() - timezone.timedelta(days=1)
    ):
        agreement.is_current = False
        agreement.save()


@shared_task
def set_user_is_active_to_false():
    for user in User.objects.filter(is_superuser=False):
        if not user.agreements.filter(is_current=True).exists():
            user.is_active = False
            user.save()


@shared_task
def set_user_vacation_left():
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
