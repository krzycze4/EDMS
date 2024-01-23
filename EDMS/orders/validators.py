import os.path
from datetime import datetime
from typing import Any, Dict

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from humanize import naturalsize

from .models import Order


def end_after_start_validator(cleaned_data: Dict[str, Any]) -> None:
    start_date = cleaned_data["start_date"]
    end_date = cleaned_data["end_date"]
    if start_date > end_date:
        raise ValidationError(
            {"end_date": "End date can't be earlier than start date!"}
        )


def forbidden_repetition_validator(cleaned_data: Dict[str, Any]) -> None:
    start_date = cleaned_data["start_date"]
    end_date = cleaned_data["end_date"]
    payment = cleaned_data["payment"]
    company = cleaned_data["company"]
    if Order.objects.filter(
        payment=payment, company=company, start_date=start_date, end_date=end_date
    ):
        raise ValidationError(
            {
                "error": "Order with this data already exists!",
            }
        )


def forbidden_future_date_validator(cleaned_data: Dict[str, Any]) -> None:
    create_date = cleaned_data["create_date"]
    if datetime.today().date() < create_date:
        raise ValidationError({"create_date": "The create date can't be future date."})


def max_size_file_validator(cleaned_data: Dict[str, Any]) -> None:
    scan = cleaned_data["scan"]
    scan_size = scan.size
    max_scan_size = 10**7  # 10mB
    if scan_size > max_scan_size:
        raise ValidationError(
            {"scan": f"Max size file is {naturalsize(max_scan_size)}"}
        )


def file_extension_validator(cleaned_data: Dict[str, Any]) -> None:
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
