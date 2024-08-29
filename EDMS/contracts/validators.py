import inspect
import os
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from companies.models import Company
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from humanize import naturalsize

User = get_user_model()


class ContractValidator:
    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Gets all validation methods in this class.

        Returns:
            List[callable]: A list of validation functions.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_create_date_before_start_date(
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]
    ) -> None:
        """
        Checks if the create_date is before the start date.

        Args:
            cleaned_data (Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]): The cleaned data from
             the form.

        Raises:
            ValidationError: If the start date is before the create_date.
        """
        create_date: date = cleaned_data["create_date"]
        start_date: date = cleaned_data["start_date"]
        if start_date < create_date:
            raise ValidationError(
                {
                    "create_date": "Create date can't be later than...",
                    "start_date": "...start date.",
                }
            )

    @staticmethod
    def validate_end_date_after_start_date(
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]
    ) -> None:
        """
        Checks if the end_date is after the start_date.

        Args:
            cleaned_data (Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]): The cleaned data from
             the form.

        Raises:
            ValidationError: If the end date is before the start date.
        """
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        if start_date > end_date:
            raise ValidationError({"end_date": "End end_date can't be earlier than start end_date!"})

    @staticmethod
    def validate_max_size_file(
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]
    ) -> None:
        """
        Checks if the uploaded file size is within the maximum limit.

        Args:
            cleaned_data (Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]): The cleaned data from
             the form.

        Raises:
            ValidationError: If the file size is too large.
        """
        scan: UploadedFile = cleaned_data["scan"]
        scan_size: int = scan.size
        max_scan_size: int = 10**7  # 10mB
        if scan_size > max_scan_size:
            raise ValidationError({"scan": f"Max size file is {naturalsize(max_scan_size)}"})

    @staticmethod
    def validate_file_extension(
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]
    ) -> None:
        """
        Checks if the uploaded file has a valid extension.

        Args:
            cleaned_data (Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]): The cleaned data from
            the form.

        Raises:
            ValidationError: If the file extension is not allowed.
        """
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
                    "scan": f"Incorrect extensions. Your file extension: {extension}."
                    f"Valid extensions: {valid_extensions_str}"
                }
            )

    @staticmethod
    def validate_no_future_create_date(
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]
    ) -> None:
        """
        Checks if the create_date is not in the future.

        Args:
            cleaned_data (Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]): The cleaned data from
            the form.

        Raises:
            ValidationError: If the create_date is in the future.
        """
        create_date: date = cleaned_data["create_date"]
        if timezone.now().date() < create_date:
            raise ValidationError({"create_date": "The create date can't be future end_date."})
