from typing import Any, Dict

from companies.models import Company
from django import forms
from orders.validators import (
    validate_end_date_after_start_date,
    validate_file_extension,
    validate_max_size_file,
    validate_no_future_create_date,
)

from .models import Contract
from .validators import validate_create_date_before_start_date


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "company": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "employee": forms.SelectMultiple(attrs={"class": "form-control js-example-basic-multiple"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "scan": forms.FileInput(attrs={"class": "form-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.exclude(is_mine=True)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        validate_no_future_create_date(cleaned_data=cleaned_data)
        validate_create_date_before_start_date(cleaned_data=cleaned_data)
        return cleaned_data
