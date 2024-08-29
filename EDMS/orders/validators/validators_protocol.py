import inspect
import os
from datetime import date
from typing import Dict, List, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from humanize import naturalsize


class ProtocolValidator:
    """
    Handles validation of ProtocolForm data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Returns a list of all validation functions in the class.

        Returns:
            List[callable]: A list of all functions that can be used for validation.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_no_future_create_date(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
        """
        Checks if the create date is not in the future.

        Args:
            cleaned_data (Dict[str, Union[date | UploadedFile]]): The data with the create date.

        Raises:
            ValidationError: If the create date is in the future.
        """
        create_date = cleaned_data["create_date"]
        if timezone.now().date() < create_date:
            raise ValidationError({"create_date": "The create date can't be future end_date."})

    @staticmethod
    def validate_max_size_file(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
        """
        Checks if the uploaded file size is within the allowed limit.

        Args:
            cleaned_data (Dict[str, Union[date | UploadedFile]]): The data with the uploaded file.

        Raises:
            ValidationError: If the file size is larger than 10MB.
        """
        scan = cleaned_data["scan"]
        scan_size = scan.size
        max_scan_size = 10**7  # 10mB
        if scan_size > max_scan_size:
            raise ValidationError({"scan": f"Max size file is {naturalsize(max_scan_size)}"})

    @staticmethod
    def validate_file_extension(cleaned_data: Dict[str, Union[date | UploadedFile]]) -> None:
        """
        Checks if the uploaded file has a valid extension.

        Args:
            cleaned_data (Dict[str, Union[date | UploadedFile]]): The data with the uploaded file.

        Raises:
            ValidationError: If the file extension is not allowed.
        """
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
