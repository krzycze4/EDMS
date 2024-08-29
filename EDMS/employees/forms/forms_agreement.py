from collections import OrderedDict
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from employees.models.models_agreement import Agreement
from employees.validators.validators_agreement import AgreementValidator

User = get_user_model()


class AgreementForm(forms.ModelForm):
    user_display = forms.CharField(
        label="User",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )

    class Meta:
        model = Agreement
        fields = OrderedDict(
            [
                ("name", "name"),
                ("type", "type"),
                ("salary_gross", "salary_gross"),
                ("create_date", "create_date"),
                ("start_date", "start_date"),
                ("end_date", "end_date"),
                ("user", "user"),
                ("user_display", "user_display"),
                ("scan", "scan"),
            ]
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "salary_gross": forms.NumberInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "user": forms.HiddenInput(),
            "scan": forms.FileInput(),
        }
        labels = {
            "user": "",
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the AgreementForm.

        Args:
            *args: Positional arguments for the form.
            **kwargs: Keyword arguments for the form, including:
                instance (Agreement): An instance of the Agreement model (optional).
                user (User): The user to associate with the agreement (required).

        Sets the initial values for user and user_display fields based on the provided user and instance.
        """
        instance: Agreement = kwargs.get("instance", None)
        user: User = kwargs.pop("user", None)
        if instance:
            initial_user_display = f"{instance.user.first_name} {instance.user.last_name}"
        else:
            initial_user_display = f"{user.first_name} {user.last_name}"
        super().__init__(*args, **kwargs)
        self.fields["user"].initial = user
        self.fields["user_display"].initial = initial_user_display

    def clean(self) -> Dict[str, Union[str | Decimal | date | User | UploadedFile]]:
        cleaned_data: Dict[str, Union[str | Decimal | date | User | UploadedFile]] = super().clean()
        validators: List[callable] = AgreementValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
