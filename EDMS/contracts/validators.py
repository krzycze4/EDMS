from datetime import date
from typing import Any, Dict

from companies.models import Company
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


def validate_same_company_in_order_and_contract(cleaned_data: Dict[str, Any]) -> None:
    company_from_order: Company = cleaned_data["company"]
    company_from_contract: Company = cleaned_data["contract"].company
    if not company_from_order == company_from_contract:
        raise ValidationError(
            {
                "company": "This company must be the same as...",
                "contract": "...the company on this contract.",
            }
        )
