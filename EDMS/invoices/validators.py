import inspect
import os
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from companies.models import Company
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from invoices.models import Invoice


class InvoiceValidator:
    """
    Handles validation of InvoiceForm data.
    """

    @classmethod
    def all_validators(cls) -> List[callable]:
        """
        Gets all the validation methods in this class.

        Returns:
            List[callable]: A list of all the validator methods in the class.
        """
        return [func for _, func in inspect.getmembers(cls, predicate=inspect.isfunction)]

    @staticmethod
    def validate_seller_different_than_buyer(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if the seller and buyer are different.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the seller is the same as the buyer.
        """
        seller: Company = cleaned_data["seller"]
        buyer: Company = cleaned_data["buyer"]

        if seller == buyer:
            raise ValidationError({"seller": "The buyer can't be the seller."})

    @staticmethod
    def validate_max_vat(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]]
    ) -> None:
        """
        Checks if the VAT is within the allowed maximum.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the VAT is greater than 23% of the net price.
        """
        vat: Decimal = cleaned_data["vat"]
        net_price: Decimal = cleaned_data["net_price"]

        max_vat_rate = Decimal(0.23)
        max_allowed_vat: Decimal = max_vat_rate * net_price

        if vat > max_allowed_vat:
            raise ValidationError({"vat": ["VAT prize can't be bigger than 23% of net price."]})

    @staticmethod
    def validate_net_price_plus_vat_equal_gross(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if the net price plus VAT equals the gross amount.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the net price plus VAT does not equal the gross amount.
        """
        net_price: Decimal = cleaned_data["net_price"]
        vat: Decimal = cleaned_data["vat"]
        gross: Decimal = cleaned_data["gross"]

        if net_price + vat != gross:
            raise ValidationError({"gross": "The net price plus the vat is not equal the gross."})

    @staticmethod
    def validate_no_future_create_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if the invoice's create date is not in the future.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the create date is in the future.
        """
        today: date = timezone.now().date()
        create_date: date = cleaned_data["create_date"]

        if today < create_date:
            raise ValidationError({"create_date": "You can't create any invoice with a future end_date."})

    @staticmethod
    def validate_no_payment_date_before_create_date(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if the payment date is not before the create date, except for certain invoice types.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the payment date is before the create date for invoices that are not duplicates or
            correcting invoices.
        """
        if cleaned_data["type"] not in [Invoice.DUPLICATE, Invoice.CORRECTING]:
            payment_date: date = cleaned_data["payment_date"]
            create_date: date = cleaned_data["create_date"]

            if payment_date < create_date:
                raise ValidationError({"payment_date": "Salary end_date can't be earlier than create end_date."})

    @staticmethod
    def validate_seller_or_buyer_must_be_my_company(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if either the seller or the buyer is the user's company.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If neither the seller nor the buyer is the user's company.
        """
        buyer: Company = cleaned_data["buyer"]
        seller: Company = cleaned_data["seller"]
        if not buyer.is_mine and not seller.is_mine:
            raise ValidationError(
                {
                    "seller": "You can't add any invoice not related with our company. Change seller or...",
                    "buyer": "...change buyer to our company.",
                },
            )

    @staticmethod
    def validate_original_invoice_not_linked_to_other_invoice(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if an original invoice is linked to another invoice.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If an original invoice is linked to another invoice.
        """
        invoice_type: str = cleaned_data["type"]
        linked_invoice: Invoice = cleaned_data["linked_invoice"]
        if linked_invoice and invoice_type == Invoice.ORIGINAL:
            raise ValidationError({"linked_invoice": "Original can't be linked to any other invoice."})

    @staticmethod
    def validate_proforma_and_duplicate_same_data_as_original(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if proforma or duplicate invoices have the same data as the original.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the data in proforma or duplicate invoices is different from the original.
        """
        linked_invoice: Invoice = cleaned_data["linked_invoice"]
        if linked_invoice:
            invoice_type: str = cleaned_data["type"]
            if invoice_type in [Invoice.DUPLICATE, Invoice.PROFORMA]:
                checked_fields = ["seller", "buyer", "net_price", "vat", "gross", "is_paid"]
                if invoice_type == Invoice.DUPLICATE:
                    checked_fields += ["service_date", "payment_date"]
                for field in checked_fields:
                    if cleaned_data[field] != getattr(linked_invoice, field):
                        formatted_field = " ".join(word for word in field.split("_"))
                        raise ValidationError(
                            {field: f"{formatted_field.title()} must be the same as in the original."}
                        )

    @staticmethod
    def validate_correcting_invoice_linked_with_original_or_duplicate(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]],
    ) -> None:
        """
        Checks if a correcting invoice is linked with an original or duplicate invoice.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If a correcting invoice is linked to a proforma invoice instead of an original or duplicate.
        """
        invoice_type: str = cleaned_data["type"]
        linked_invoice: Invoice = cleaned_data["linked_invoice"]
        if invoice_type == Invoice.CORRECTING and linked_invoice.type == Invoice.PROFORMA:
            raise ValidationError(
                {"linked_invoice": "Correcting invoice must be linked to duplicate or original invoice."}
            )

    @staticmethod
    def validate_file_extension(
        cleaned_data: Dict[str, Union[str | Decimal | date | Company | UploadedFile | Invoice | bool]]
    ) -> None:
        """
        Checks if the file extension of the uploaded scan is valid.

        Args:
            cleaned_data (Dict): The cleaned data dictionary containing the invoice details.

        Raises:
            ValidationError: If the file extension is not in the list of allowed extensions.
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
                    "scan": f"Incorrect extensions. Your file extension: {extension}. Valid extensions: {valid_extensions_str}"
                }
            )
