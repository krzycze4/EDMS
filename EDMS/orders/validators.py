import os.path
from datetime import date
from typing import Any, Dict

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from humanize import naturalsize

from .models import Order


def validate_end_date_after_start_date(cleaned_data: Dict[str, Any]) -> None:
    start_date = cleaned_data["start_date"]
    end_date = cleaned_data["end_date"]
    if start_date > end_date:
        raise ValidationError(
            {"end_date": "End end_date can't be earlier than start end_date!"}
        )


def validate_no_repetition(cleaned_data: Dict[str, Any]) -> None:
    start_date = cleaned_data["start_date"]
    end_date = cleaned_data["end_date"]
    payment = cleaned_data["payment"]
    company = cleaned_data["company"]
    if Order.objects.filter(
        payment=payment, company=company, start_date=start_date, end_date=end_date
    ):
        raise ValidationError(
            {
                "name": "Order with this data already exists!",
            }
        )


def validate_no_future_create_date(cleaned_data: Dict[str, Any]) -> None:
    create_date = cleaned_data["create_date"]
    if timezone.now().date() < create_date:
        raise ValidationError(
            {"create_date": "The create end_date can't be future end_date."}
        )


def validate_max_size_file(cleaned_data: Dict[str, Any]) -> None:
    scan = cleaned_data["scan"]
    scan_size = scan.size
    max_scan_size = 10**7  # 10mB
    if scan_size > max_scan_size:
        raise ValidationError(
            {"scan": f"Max size file is {naturalsize(max_scan_size)}"}
        )


def validate_file_extension(cleaned_data: Dict[str, Any]) -> None:
    scan: UploadedFile = cleaned_data["scan"]
    extension = os.path.splitext(scan.name)[1]
    valid_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".jfif",
        ".pjpeg",
        ".pjp",
        ".png",
        ".svg",
    ]
    if extension not in valid_extensions:
        valid_extensions_str = ", ".join(valid_extensions)
        raise ValidationError(
            {
                "scan": f"Incorrect extensions. Your file extension: {extension}. Valid extensions: {valid_extensions_str}"
            }
        )


def validate_start_date_in_contract_period(cleaned_data: Dict[str, Any]) -> None:
    start_date_order: date = cleaned_data["start_date"]
    start_date_contract: date = cleaned_data["contract"].start_date
    end_date_contract: date = cleaned_data["contract"].end_date

    if not start_date_contract <= start_date_order <= end_date_contract:
        raise ValidationError({"start_date": "Start date must be in contract period."})
