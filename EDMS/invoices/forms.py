from datetime import date
from decimal import Decimal
from typing import Dict, Union

from django import forms

from .models import Company, Invoice
from .validators import (
    future_create_date_validator,
    net_price_and_vat_equal_gross_validator,
    payment_date_before_create_date_validator,
    seller_different_than_buyer_validator,
    seller_or_buyer_must_be_my_company_validator,
    vat_max_validator,
)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "seller": forms.Select(attrs={"class": "form-control"}),
            "buyer": forms.Select(attrs={"class": "form-control"}),
            "net_price": forms.TextInput(attrs={"class": "form-control"}),
            "vat": forms.TextInput(attrs={"class": "form-control"}),
            "gross": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "service_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "payment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_paid": forms.CheckboxInput(attrs={"class": "form-check-input ml-2"}),
        }

    def clean(self) -> Dict[str, Union[Decimal | date | Company]]:
        cleaned_data: Dict[str, Union[Decimal | date | Company]] = super().clean()
        vat_max_validator(attrs=cleaned_data)
        future_create_date_validator(attrs=cleaned_data)
        payment_date_before_create_date_validator(attrs=cleaned_data)
        net_price_and_vat_equal_gross_validator(attrs=cleaned_data)
        seller_different_than_buyer_validator(attrs=cleaned_data)
        seller_or_buyer_must_be_my_company_validator(attrs=cleaned_data)
        return cleaned_data
