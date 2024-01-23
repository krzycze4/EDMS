from datetime import date
from decimal import Decimal
from typing import Dict, Union

from django import forms
from orders.validators import file_extension_validator

from .models import Company, Invoice
from .validators import (
    correcting_invoice_linked_with_original_or_duplicate_validator,
    future_create_date_validator,
    net_price_and_vat_equal_gross_validator,
    original_invoice_not_linked_to_other_invoice,
    payment_date_before_create_date_validator,
    proforma_and_duplicate_same_data_as_original_validator,
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
            "seller": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "buyer": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "net_price": forms.NumberInput(attrs={"class": "form-control"}),
            "vat": forms.NumberInput(attrs={"class": "form-control"}),
            "gross": forms.NumberInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "service_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "payment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "type": forms.Select(attrs={"class": "form-control"}),
            "scan": forms.FileInput(attrs={"class": "form-input"}),
            "linked_invoice": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "is_paid": forms.CheckboxInput(attrs={"class": "form-check-input ml-2"}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["linked_invoice"].queryset = Invoice.objects.exclude(
                pk=self.instance.pk
            )

    def clean(self) -> Dict[str, Union[Decimal | date | Company]]:
        cleaned_data: Dict[str, Union[Decimal | date | Company]] = super().clean()
        original_invoice_not_linked_to_other_invoice(attrs=cleaned_data)
        proforma_and_duplicate_same_data_as_original_validator(attrs=cleaned_data)
        correcting_invoice_linked_with_original_or_duplicate_validator(
            attrs=cleaned_data
        )
        vat_max_validator(attrs=cleaned_data)
        future_create_date_validator(attrs=cleaned_data)
        payment_date_before_create_date_validator(attrs=cleaned_data)
        net_price_and_vat_equal_gross_validator(attrs=cleaned_data)
        seller_different_than_buyer_validator(attrs=cleaned_data)
        seller_or_buyer_must_be_my_company_validator(attrs=cleaned_data)
        file_extension_validator(cleaned_data=cleaned_data)
        return cleaned_data
