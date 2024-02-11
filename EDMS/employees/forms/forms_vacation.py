from typing import Any, Dict

from django import forms
from employees.models.models_vacation import Vacation
from employees.validators.validators_vacation import (
    validate_enough_vacation_left,
    validate_no_overlap_vacation_dates,
    validate_user_can_take_vacation,
)
from orders.validators import (
    validate_end_date_after_start_date,
    validate_file_extension,
    validate_max_size_file,
)
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
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
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
        self.fields["substitute_users"].queryset = User.objects.exclude(
            pk=kwargs["initial"]["leave_user"]
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data: Dict[str, Any] = super().clean()
        validate_user_can_take_vacation(cleaned_data=cleaned_data)  # OK
        if self.instance.pk:
            cleaned_data["id"] = self.instance.pk
        validate_end_date_after_start_date(cleaned_data=cleaned_data)  # OK
        validate_no_overlap_vacation_dates(cleaned_data=cleaned_data)  # OK
        validate_file_extension(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        validate_enough_vacation_left(
            cleaned_data=cleaned_data
        )  # PROBLEM - can't see pk
        return cleaned_data
