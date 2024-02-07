from datetime import date
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from employees.models.models_agreement import Agreement
from employees.models.models_vacation import Vacation

User = get_user_model()


def validate_create_date_not_after_start_date(cleaned_data: Dict[str, Any]) -> None:
    create_date: date = cleaned_data["create_date"]
    start_date: date = cleaned_data["start_date"]

    if create_date > start_date:
        raise ValidationError(
            {
                "create_date": "Create end_date must be before or the same as start end_date."
            }
        )


def validate_no_vacation_repetitions(cleaned_data: Dict[str, Any]) -> None:
    leave_type: str = cleaned_data["type"]
    start_date: date = cleaned_data["start_date"]
    end_date: date = cleaned_data["start_date"]
    leave_user: User = cleaned_data["leave_user"]
    if Vacation.objects.filter(
        type=leave_type, start_date=start_date, end_date=end_date, leave_user=leave_user
    ).exists():
        raise ValidationError({"scan": "Do not duplicate leaves"})


def validate_no_overlap_vacation_dates(cleaned_data: Dict[str, Any]) -> None:
    start_date: date = cleaned_data["start_date"]
    end_date: date = cleaned_data["end_date"]
    leave_user: date = cleaned_data["leave_user"]
    if "id" in cleaned_data.keys():
        vacation_id: int = cleaned_data["id"]
        vacations = Vacation.objects.filter(leave_user=leave_user).exclude(
            pk=vacation_id
        )
    else:
        vacations = Vacation.objects.filter(leave_user=leave_user)
    if vacations:
        for vacation in vacations:
            if (
                (vacation.start_date <= start_date <= vacation.end_date)
                or (vacation.start_date <= end_date <= vacation.end_date)
                or (start_date <= vacation.start_date and vacation.end_date <= end_date)
            ):
                raise ValidationError(
                    {
                        "start_date": "The vacation overlaps...",
                        "end_date": f"...overlaps vacation #{vacation.pk}",
                    }
                )


def validate_termination_dates(cleaned_data: Dict[str, Any]) -> None:
    agreement: Agreement = cleaned_data["agreement"]
    create_date: date = cleaned_data["create_date"]
    end_date: date = cleaned_data["end_date"]
    if end_date < agreement.start_date:
        raise ValidationError(
            {"end_date": "End date can't be earlier than start date of the agreement."}
        )
    if create_date > end_date:
        raise ValidationError(
            {
                "end_date": "End date can't be earlier than create date of the termination."
            }
        )
    if create_date < agreement.start_date:
        raise ValidationError(
            {
                "create_date": "Create date can't be earlier than start date of the agreement."
            }
        )
    if end_date > agreement.end_date_actual and not agreement.termination:
        raise ValidationError(
            {
                "end_date": "End date termination can't be later than actual end date of the agreement."
            }
        )


def validate_addendum_dates(cleaned_data: Dict[str, Any]) -> None:
    agreement: Agreement = cleaned_data["agreement"]
    create_date: date = cleaned_data["create_date"]
    end_date: date = cleaned_data["end_date"]
    if end_date < agreement.start_date:
        raise ValidationError(
            {"end_date": "End date can't be earlier than start date of the agreement."}
        )
    if create_date > end_date:
        raise ValidationError(
            {"end_date": "End date can't be earlier than create date of the addendum."}
        )
    if create_date < agreement.start_date:
        raise ValidationError(
            {
                "create_date": "Create date can't be earlier than start date of the agreement."
            }
        )
    if end_date < agreement.end_date_actual:
        raise ValidationError(
            {
                "end_date": "End date addendum can't be earlier than actual end date of the agreement."
            }
        )


def validate_user_can_take_vacation(cleaned_data: Dict[str, Any]) -> None:
    leave_user: User = cleaned_data["leave_user"]
    var = Agreement.objects.filter(
        user=leave_user, is_current=True, type=Agreement.EMPLOYMENT
    ).exists()
    print(var)
    if not var:
        raise ValidationError(
            {
                "scan": "You can't take vacation because you don't have current employment agreement."
            }
        )
