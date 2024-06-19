from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, List, Union

from companies.models import Company
from contracts.models import Contract
from django import forms
from orders.models import Order, Protocol
from orders.validators.validators_order import (
    OrderCreateValidator,
    OrderUpdateValidator,
)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "payment",
            "company",
            "start_date",
            "end_date",
            "contract",
            "description",
        ]
        widgets = {
            "payment": forms.NumberInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "contract": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["contract"].queryset = Contract.objects.filter(company=self.instance.company)

    def clean(self) -> Dict[str, Any]:
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]] = super().clean()
        validators: List[callable] = OrderCreateValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "company",
            "payment",
            "status",
            "start_date",
            "end_date",
            "description",
        ]
        widgets = {
            "company": forms.HiddenInput(),
            "payment": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data: Dict[str, Union[Decimal | Company | str | date | Contract]] = super().clean()
        validators: List[callable] = OrderUpdateValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.end_date > datetime.today().date() or not Protocol.objects.filter(order=self.instance):
            self.fields["status"].widget = forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"})
