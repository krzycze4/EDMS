from datetime import date
from typing import Any, Dict

from django.core.exceptions import ValidationError


def validate_create_date_before_start_date(cleaned_data: Dict[str, Any]) -> None:
    create_date: date = cleaned_data["create_date"]
    start_date: date = cleaned_data["start_date"]
    if start_date < create_date:
        raise ValidationError(
            {
                "create_date": "Create date can't be later than...",
                "start_date": "...start date.",
            }
        )
