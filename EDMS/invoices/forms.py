from datetime import date
from decimal import Decimal
from typing import Dict, Union

from django import forms
from orders.validators import validate_file_extension

from .models import Company, Invoice
from .validators import (
    validate_correcting_invoice_linked_with_original_or_duplicate,
    validate_max_vat,
    validate_net_price_plus_vat_equal_gross,
    validate_no_future_create_date,
    validate_no_payment_date_before_create_date,
    validate_original_invoice_not_linked_to_other_invoice,
    validate_proforma_and_duplicate_same_data_as_original,
    validate_seller_different_than_buyer,
    validate_seller_or_buyer_must_be_my_company,
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
                attrs={"class": "form-control", "type": "end_date"}
            ),
            "service_date": forms.DateInput(
                attrs={"class": "form-control", "type": "end_date"}
            ),
            "payment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "end_date"}
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
        validate_original_invoice_not_linked_to_other_invoice(attrs=cleaned_data)
        validate_proforma_and_duplicate_same_data_as_original(attrs=cleaned_data)
        validate_correcting_invoice_linked_with_original_or_duplicate(
            attrs=cleaned_data
        )
        validate_max_vat(attrs=cleaned_data)
        validate_no_future_create_date(attrs=cleaned_data)
        validate_no_payment_date_before_create_date(attrs=cleaned_data)
        validate_net_price_plus_vat_equal_gross(attrs=cleaned_data)
        validate_seller_different_than_buyer(attrs=cleaned_data)
        validate_seller_or_buyer_must_be_my_company(attrs=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        return cleaned_data
