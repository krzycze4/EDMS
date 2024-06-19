import inspect
import os
from datetime import date
from typing import Dict, List, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from humanize import naturalsize


class ProtocolValidator:
    @classmethod
    def all_validators(cls) -> List[callable]:
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_no_future_create_date(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
        create_date = cleaned_data["create_date"]
        if timezone.now().date() < create_date:
            raise ValidationError({"create_date": "The create date can't be future end_date."})

    @staticmethod
    def validate_max_size_file(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
        scan = cleaned_data["scan"]
        scan_size = scan.size
        max_scan_size = 10**7  # 10mB
        if scan_size > max_scan_size:
            raise ValidationError({"scan": f"Max size file is {naturalsize(max_scan_size)}"})

    @staticmethod
    def validate_file_extension(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
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
