import inspect
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from companies.models import Company
from contracts.models import Contract
from django.core.exceptions import ValidationError
from django.utils import timezone
from orders.models import Order


class OrderCreateValidator:
    """
    Handles validation of OrderCreateForm data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Checks if the end date is after the start date.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the end date is before the start date.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_end_date_after_start_date(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Checks if an order with the same data already exists.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If an order with the same payment, company, start date, and end date exists.
        """
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        if start_date > end_date:
            raise ValidationError({"end_date": "End end_date can't be earlier than start end_date!"})

    @staticmethod
    def validate_no_repetition(cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]) -> None:
        """
        Checks if the create date is not in the future.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the create date is in the future.
        """
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        payment: Decimal = cleaned_data["payment"]
        company = cleaned_data["company"]
        if Order.objects.filter(payment=payment, company=company, start_date=start_date, end_date=end_date):
            raise ValidationError(
                {
                    "description": "Order with this data already exists!",
                }
            )

    @staticmethod
    def validate_no_future_create_date(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Checks if the start date of the order is within the contract period.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the start date of the order is not within the contract period.
        """
        create_date = cleaned_data["create_date"]
        if timezone.now().date() < create_date:
            raise ValidationError({"create_date": "The create date can't be future end_date."})

    @staticmethod
    def validate_start_date_in_contract_period(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Checks if the company in the order is the same as the company in the contract.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the company in the order and the company in the contract are different.
        """
        start_date_order: date = cleaned_data["start_date"]
        start_date_contract: date = cleaned_data["contract"].start_date
        end_date_contract: date = cleaned_data["contract"].end_date

        if not start_date_contract <= start_date_order <= end_date_contract:
            raise ValidationError({"start_date": "Start date must be in contract period."})

    @staticmethod
    def validate_same_company_in_order_and_contract(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Gets a list of all validator methods in this class.

        Returns:
            List[callable]: A list of all validator functions.
        """
        company_in_order: Company = cleaned_data["company"]
        company_in_contract: Company = cleaned_data["contract"].company
        if not company_in_order == company_in_contract:
            raise ValidationError({"company": "Company in order must be the same as company in contract."})


class OrderUpdateValidator:
    """
    Handles validation of OrderUpdateForm data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Gets a list of all validator methods in this class.

        Returns:
            List[callable]: A list of all validator functions.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_start_date_in_contract_period(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Checks if the start date of the order is within the contract period.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the start date of the order is not within the contract period.
        """
        start_date_order: date = cleaned_data["start_date"]
        start_date_contract: date = cleaned_data["contract"].start_date
        end_date_contract: date = cleaned_data["contract"].end_date

        if not start_date_contract <= start_date_order <= end_date_contract:
            raise ValidationError({"start_date": "Start date must be in contract period."})

    @staticmethod
    def validate_end_date_after_start_date(
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]]
    ) -> None:
        """
        Checks if the end date is after the start date.

        Args:
            cleaned_data (Dict[str, Union[Decimal | Company | str | date | Contract]]): The cleaned data from the form.

        Raises:
            ValidationError: If the end date is before the start date.
        """
        start_date: date = cleaned_data["start_date"]
        end_date: date = cleaned_data["end_date"]
        if start_date > end_date:
            raise ValidationError({"end_date": "End end_date can't be earlier than start end_date!"})
