from datetime import date
from decimal import Decimal
from typing import Dict, Union

from companies.models import Company
from django.core.exceptions import ValidationError
from django.utils import timezone


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
