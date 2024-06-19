from datetime import date
from typing import Dict, List, Union

from django import forms
from django.core.files.uploadedfile import UploadedFile
from employees.models.models_vacation import Vacation
from employees.validators.validators_vacation import VacationValidator
from users.models import User


class VacationForm(forms.ModelForm):
    leave_user_display = forms.CharField(
        label="Leave user",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )

    class Meta:
        model = Vacation
        fields = [
            "type",
            "start_date",
            "end_date",
            "included_days_off",
            "leave_user",
            "leave_user_display",
            "substitute_users",
            "scan",
        ]
        widgets = {
            "type": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "leave_user": forms.HiddenInput(),
            "substitute_users": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 3}
            ),
            "scan": forms.FileInput(),
            "included_days_off": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "id": "",
            "leave_user": "",
            "included_days_off": "Days off due top-down in this vacation term",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["substitute_users"].queryset = User.objects.exclude(pk=kwargs["initial"]["leave_user"])

    def clean(self) -> Dict[str, Union[str | date | User | List[User] | UploadedFile | int]]:
        cleaned_data: Dict[str, Union[str | date | User | List[User] | UploadedFile | int]] = super().clean()
        if self.instance.pk:
            cleaned_data["id"] = self.instance.pk
        validators: List[callable] = VacationValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
