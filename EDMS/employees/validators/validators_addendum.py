from datetime import date
from typing import Any, Dict

from django.core.exceptions import ValidationError
from employees.models.models_agreement import Agreement


def validate_addendum_dates(cleaned_data: Dict[str, Any]) -> None:
    agreement: Agreement = cleaned_data["agreement"]
    create_date: date = cleaned_data["create_date"]
    end_date: date = cleaned_data["end_date"]
    if end_date < agreement.start_date:
        raise ValidationError({"end_date": "End date can't be earlier than start date of the agreement."})
    if create_date > end_date:
        raise ValidationError({"end_date": "End date can't be earlier than create date of the addendum."})
    if create_date < agreement.start_date:
        raise ValidationError({"create_date": "Create date can't be earlier than start date of the agreement."})
    if end_date < agreement.end_date_actual:
        raise ValidationError({"end_date": "End date addendum can't be earlier than actual end date of the agreement."})
