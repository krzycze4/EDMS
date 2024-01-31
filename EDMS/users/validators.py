from datetime import date
from typing import Any, Dict

from django.core.exceptions import ValidationError


def create_date_before_or_the_same_as_start_date(cleaned_data: Dict[str, Any]) -> None:
    create_date: date = cleaned_data["create_date"]
    start_date: date = cleaned_data["start_date"]

    if create_date > start_date:
        raise ValidationError(
            {"create_date": "Create date must be before or the same as start date."}
        )
