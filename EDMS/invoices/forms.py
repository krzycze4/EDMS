from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from django import forms

from .models import Company, Invoice
from .validators import InvoiceValidator


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "seller": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "buyer": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "net_price": forms.NumberInput(attrs={"class": "form-control"}),
            "vat": forms.NumberInput(attrs={"class": "form-control"}),
            "gross": forms.NumberInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "service_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "payment_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "scan": forms.FileInput(attrs={"class": "form-input"}),
            "linked_invoice": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "is_paid": forms.CheckboxInput(attrs={"class": "form-check-input ml-2"}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["linked_invoice"].queryset = Invoice.objects.exclude(pk=self.instance.pk)

    def clean(self) -> Dict[str, Union[Decimal | date | Company]]:
        cleaned_data: Dict[str, Union[Decimal | date | Company]] = super().clean()
        validators: List[callable] = InvoiceValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
