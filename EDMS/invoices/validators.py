from datetime import date
from decimal import Decimal
from typing import Dict, Union

from companies.models import Company
from django.core.exceptions import ValidationError
from django.utils import timezone
from invoices.models import Invoice


def seller_different_than_buyer_validator(
    attrs: Dict[str, Union[Decimal | date | Company]],
) -> None:
    seller: Company = attrs["seller"]
    buyer: Company = attrs["buyer"]

    if seller == buyer:
        raise ValidationError({"seller": "The buyer can't be the seller."})


def vat_max_validator(attrs: Dict[str, Union[Decimal | date | Company]]) -> None:
    vat: Decimal = attrs["vat"]
    net_price: Decimal = attrs["net_price"]

    max_vat_rate = Decimal(0.23)
    max_allowed_vat: Decimal = max_vat_rate * net_price

    if vat > max_allowed_vat:
        raise ValidationError(
            {"vat": ["VAT prize can't be bigger than 23% of net price."]}
        )


def net_price_and_vat_equal_gross_validator(
    attrs: Dict[str, Union[Decimal | date | Company]],
) -> None:
    net_price: Decimal = attrs["net_price"]
    vat: Decimal = attrs["vat"]
    gross: Decimal = attrs["gross"]

    if net_price + vat != gross:
        raise ValidationError(
            {"gross": "The net price plus the vat is not equal the gross."}
        )


def future_create_date_validator(
    attrs: Dict[str, Union[Decimal | date | Company]],
) -> None:
    today: date = timezone.now().date()
    create_date: date = attrs["create_date"]

    if today < create_date:
        raise ValidationError(
            {"create_date": "You can't create any invoice with a future date."}
        )


def payment_date_before_create_date_validator(
    attrs: Dict[str, Union[Decimal | date | Company]],
) -> None:
    if attrs["type"] not in [Invoice.DUPLICATE, Invoice.CORRECTING]:
        payment_date: date = attrs["payment_date"]
        create_date: date = attrs["create_date"]

        if payment_date < create_date:
            raise ValidationError(
                {"payment_date": "Payment date can't be earlier than create date."}
            )


def seller_or_buyer_must_be_my_company_validator(
    attrs: Dict[str, Union[Decimal | date | Company]],
) -> None:
    buyer: Company = attrs["buyer"]
    seller: Company = attrs["seller"]

    if not buyer.is_mine and not seller.is_mine:
        raise ValidationError(
            {
                "seller": "You can't add any invoice not related with our company. Change seller or...",
                "buyer": "...change buyer to our company.",
            },
        )


def original_invoice_not_linked_to_other_invoice(
    attrs: Dict[str, Union[Decimal | date | Company | str | Invoice]],
) -> None:
    invoice_type: str = attrs["type"]
    linked_invoice: Invoice = attrs["linked_invoice"]
    if linked_invoice and invoice_type == Invoice.ORIGINAL:
        raise ValidationError(
            {"linked_invoice": "Original can't be linked to any other invoice."}
        )


def proforma_and_duplicate_same_data_as_original_validator(
    attrs: Dict[str, Union[str | date | Decimal | Company | Invoice]],
) -> None:
    linked_invoice: Invoice = attrs["linked_invoice"]
    if linked_invoice:
        invoice_type: str = attrs["type"]
        if invoice_type in [Invoice.DUPLICATE, Invoice.PROFORMA]:
            checked_fields = ["seller", "buyer", "net_price", "vat", "gross", "is_paid"]
            if invoice_type == Invoice.DUPLICATE:
                checked_fields += ["service_date", "payment_date"]
            for field in checked_fields:
                if attrs[field] != getattr(linked_invoice, field):
                    formatted_field = " ".join(word for word in field.split("_"))
                    raise ValidationError(
                        {
                            field: f"{formatted_field.title()} must be the same as in the original."
                        }
                    )


def correcting_invoice_linked_with_original_or_duplicate_validator(
    attrs: Dict[str, Union[str | date | Decimal | Company | Invoice]],
) -> None:
    invoice_type: str = attrs["type"]
    linked_invoice: Invoice = attrs["linked_invoice"]
    if invoice_type == Invoice.CORRECTING and linked_invoice.type == Invoice.PROFORMA:
        raise ValidationError(
            {
                "linked_invoice": "Correcting invoice must be linked to duplicate or original invoice."
            }
        )
