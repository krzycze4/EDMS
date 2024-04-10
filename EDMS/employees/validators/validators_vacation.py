from datetime import date
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from employees.models.models_agreement import Agreement
from employees.models.models_vacation import Vacation

User = get_user_model()


def validate_no_overlap_vacation_dates(cleaned_data: Dict[str, Any]) -> None:
    start_date: date = cleaned_data["start_date"]
    end_date: date = cleaned_data["end_date"]
    leave_user: date = cleaned_data["leave_user"]
    if "id" in cleaned_data.keys():
        vacation_id: int = cleaned_data["id"]
        vacations = Vacation.objects.filter(leave_user=leave_user).exclude(pk=vacation_id)
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


def validate_user_can_take_vacation(cleaned_data: Dict[str, Any]) -> None:
    leave_user: User = cleaned_data["leave_user"]
    if not Agreement.objects.filter(user=leave_user, is_current=True, type=Agreement.EMPLOYMENT).exists():
        raise ValidationError({"scan": "You can't take vacation because you don't have current employment agreement."})


def validate_enough_vacation_left(cleaned_data: Dict[str, Any]) -> None:
    vacation_left = cleaned_data["leave_user"].vacation_left
    considered_vacation = (
        (cleaned_data["end_date"] - cleaned_data["start_date"]).days + cleaned_data["included_days_off"] + 1
    )
    if considered_vacation > vacation_left:
        raise ValidationError({"scan": "You can't take vacation because you don't have enough vacation left."})
