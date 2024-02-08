from datetime import date
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
