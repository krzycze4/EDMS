import inspect
from datetime import date
from typing import Dict, List, Union

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from employees.models.models_agreement import Agreement


class TerminationValidator:
    """
    Validator checks TerminationFrom data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Gets a list of all validator methods in the class.

        Returns:
            List[callable]: A list of all functions in the class that are used for validation.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_termination_dates(cleaned_data: Dict[str, Union[str | date | Agreement | UploadedFile]]) -> None:
        """
        Checks if the termination dates are valid.

        Args:
            cleaned_data (Dict[str, Union[str | date | Agreement | UploadedFile]]): A dictionary containing termination data to be validated.

        Raises:
            ValidationError: If any of the dates are invalid based on the agreement dates.
        """
        agreement: Agreement = cleaned_data["agreement"]
        create_date: date = cleaned_data["create_date"]
        end_date: date = cleaned_data["end_date"]
        if end_date < agreement.start_date:
            raise ValidationError({"end_date": "End date can't be earlier than start date of the agreement."})
        if create_date > end_date:
            raise ValidationError({"end_date": "End date can't be earlier than create date of the termination."})
        if create_date < agreement.start_date:
            raise ValidationError({"create_date": "Create date can't be earlier than start date of the agreement."})
        if end_date > agreement.end_date_actual and not hasattr(agreement, "termination"):
            raise ValidationError(
                {"end_date": "End date termination can't be later than actual end date of the agreement."}
            )
