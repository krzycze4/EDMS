import inspect
import os
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from humanize import naturalsize

User = get_user_model()


class AgreementValidator:
    @classmethod
    def all_validators(cls) -> List[callable]:
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_create_date_not_after_start_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]
    ) -> None:
        create_date: date = cleaned_data["create_date"]
        start_date: date = cleaned_data["start_date"]

        if create_date > start_date:
            raise ValidationError({"create_date": "Create date must be before or the same as start date."})

    @staticmethod
    def validate_end_date_after_start_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]
    ) -> None:
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        if start_date > end_date:
            raise ValidationError({"end_date": "End end_date can't be earlier than start end_date!"})

    @staticmethod
    def validate_no_future_create_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]
    ) -> None:
        create_date: date = cleaned_data["create_date"]
        if timezone.now().date() < create_date:
            raise ValidationError({"create_date": "The create date can't be future end_date."})

    @staticmethod
    def validate_file_extension(cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]) -> None:
        scan: UploadedFile = cleaned_data["scan"]
        extension: str = os.path.splitext(scan.name)[1]
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

    @staticmethod
    def validate_max_size_file(cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]) -> None:
        scan: UploadedFile = cleaned_data["scan"]
        scan_size: int = scan.size
        max_scan_size: int = 10**7  # 10mB
        if scan_size > max_scan_size:
            raise ValidationError({"scan": f"Max size file is {naturalsize(max_scan_size)}"})
