from datetime import datetime
from typing import Any, Dict

from companies.models import Company
from django import forms
from invoices.models import Invoice

from .models import Order, Protocol
from .validators import (
    end_after_start_validator,
    forbidden_future_date_validator,
    forbidden_repetition_validator,
    max_size_file_validator,
)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["payment", "company", "start_date", "end_date", "description"]
        widgets = {
            "payment": forms.NumberInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.filter(is_mine=False)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        end_after_start_validator(cleaned_data=cleaned_data)
        forbidden_repetition_validator(cleaned_data=cleaned_data)
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
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        end_after_start_validator(cleaned_data=cleaned_data)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.end_date > datetime.today().date():
            self.fields["status"].widget = forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            )


class OrderManageInvoicesForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["income_invoice", "cost_invoices"]
        widgets = {
            "income_invoice": forms.Select(
                attrs={"class": "form-control  js-example-basic-single"}
            ),
            "cost_invoices": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 6}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["income_invoice"].queryset = Invoice.objects.filter(
            seller__is_mine=True, buyer=self.instance.company
        )
        self.fields["cost_invoices"].queryset = Invoice.objects.filter(
            buyer__is_mine=True
        )


class ProtocolCreateForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ["scan", "create_date"]
        widgets = {
            "scan": forms.FileInput(attrs={"type": "file"}),
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        forbidden_future_date_validator(cleaned_data=cleaned_data)
        max_size_file_validator(cleaned_data=cleaned_data)
        return cleaned_data
