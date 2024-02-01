from datetime import datetime
from typing import Any, Dict

from django import forms
from invoices.models import Invoice

from .models import Order, Protocol
from .validators import (
    validate_end_date_after_start_date,
    validate_file_extension,
    validate_max_size_file,
    validate_no_future_create_date,
    validate_no_repetition,
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

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        validate_no_repetition(cleaned_data=cleaned_data)
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
        cleaned_data: Dict[str, Any] = super().clean()
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        return cleaned_data

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if (
            self.instance.end_date > datetime.today().date()
            or not Protocol.objects.filter(order=self.instance)
        ):
            self.fields["status"].widget = forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            )


class OrderManageInvoicesForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["cost_invoices", "income_invoices"]
        widgets = {
            "cost_invoices": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 3}
            ),
            "income_invoices": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.company.is_mine:
            self.fields.append("income_invoices")
            self.fields["income_invoices"].widget = forms.SelectMultiple(
                attrs={"class": "form-control  js-example-basic-multiple", "size": 3}
            )
            self.fields["income_invoices"].queryset = Invoice.objects.filter(
                seller__is_mine=True, buyer=self.instance.company
            )
        self.fields["cost_invoices"].queryset = Invoice.objects.filter(
            buyer__is_mine=True
        )

    def aggregate_linked_invoices(self):
        family_income_invoices = []
        chosen_income_invoices = list(self.cleaned_data["income_invoices"])
        family_income_invoices.extend(chosen_income_invoices)
        for income_invoice in family_income_invoices:
            if (
                income_invoice.linked_invoice
                and income_invoice.linked_invoice not in family_income_invoices
            ):
                family_income_invoices.append(income_invoice.linked_invoice)
            children_income_invoices = list(
                Invoice.objects.filter(linked_invoice=income_invoice)
            )
            if children_income_invoices:
                for children_income_invoice in children_income_invoices:
                    if children_income_invoice not in family_income_invoices:
                        family_income_invoices.append(children_income_invoice)
        return family_income_invoices

    def save(self, commit=True):
        order = super().save(commit=commit)
        family_income_invoices = self.aggregate_linked_invoices()
        income_invoices = Invoice.objects.filter(
            pk__in=[invoice.pk for invoice in family_income_invoices]
        )
        order.income_invoices.set(income_invoices)
        return order


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
        validate_no_future_create_date(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        return cleaned_data
