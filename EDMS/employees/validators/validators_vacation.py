import inspect
import os
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from employees.models.models_agreement import Agreement
from employees.models.models_vacation import Vacation
from humanize import naturalsize

User = get_user_model()


class VacationValidator:
    @classmethod
    def all_validators(cls) -> List[callable]:
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_no_overlap_vacation_dates(
        cleaned_data: Dict[str, Union[str | date | User | List[User] | UploadedFile | int]]
    ) -> None:
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        leave_user: date = cleaned_data["leave_user"]
        if "id" in cleaned_data.keys():
            vacation_id: int = cleaned_data["id"]
            vacations: QuerySet = Vacation.objects.filter(leave_user=leave_user).exclude(pk=vacation_id)
        else:
            vacations: QuerySet = Vacation.objects.filter(leave_user=leave_user)
        if vacations:
            for vacation in vacations:
                if (
                    (vacation.start_date <= start_date <= vacation.end_date)
                    or (vacation.start_date <= end_date <= vacation.end_date)
                    or (start_date <= vacation.start_date and vacation.end_date <= end_date)
                ):
                    raise ValidationError(
                        {
                            "start_date": "The vacation overlaps...",
                            "end_date": f"...overlaps vacation #{vacation.pk}",
                        }
                    )

    @staticmethod
    def validate_user_can_take_vacation(
        cleaned_data: Dict[str, Union[str | date | User | List[User] | UploadedFile | int]]
    ) -> None:
        leave_user: User = cleaned_data["leave_user"]
        if not Agreement.objects.filter(user=leave_user, is_current=True, type=Agreement.EMPLOYMENT).exists():
            raise ValidationError(
                {"scan": "You can't take vacation because you don't have current employment agreement."}
            )

    @staticmethod
    def validate_enough_vacation_left(
        cleaned_data: Dict[str, Union[str | date | User | List[User] | UploadedFile | int]]
    ) -> None:
        vacation_left: User = cleaned_data["leave_user"].vacation_left
        considered_vacation: int = (
            (cleaned_data["end_date"] - cleaned_data["start_date"]).days + cleaned_data["included_days_off"] + 1
        )
        if considered_vacation > vacation_left:
            raise ValidationError({"scan": "You can't take vacation because you don't have enough vacation left."})

    @staticmethod
    def validate_end_date_after_start_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]]
    ) -> None:
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        if start_date > end_date:
            raise ValidationError({"end_date": "End end_date can't be earlier than start end_date!"})

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
