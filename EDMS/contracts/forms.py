from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from companies.models import Company
from contracts.validators import ContractValidator
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile

from .models import Contract

User = get_user_model()


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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.exclude(is_mine=True)

    def clean(self) -> Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]]:
        cleaned_data: Dict[str, Union[str | date | Company | User | Decimal | UploadedFile]] = super().clean()
        validators: List[callable] = ContractValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
