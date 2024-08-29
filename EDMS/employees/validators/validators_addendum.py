import inspect
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from employees.models.models_agreement import Agreement


class AddendumValidator:
    """
    Handles validation of addendum data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Gets all validator functions in this class.

        Returns:
            List[callable]: A list of all validator functions in this class.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_addendum_dates(
        cleaned_data: Dict[str, Union[str | date | Agreement | Decimal | UploadedFile]]
    ) -> None:
        """
        Validates the dates in the addendum.

        Args:
            cleaned_data (Dict[str, Union[str | date | Agreement | Decimal | UploadedFile]]):
                A dictionary that has the data to validate.

        Raises:
            ValidationError: If any of the dates are not valid.
        """
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
            raise ValidationError(
                {"end_date": "End date addendum can't be earlier than actual end date of the agreement."}
            )
