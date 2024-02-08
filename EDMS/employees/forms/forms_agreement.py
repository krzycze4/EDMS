from collections import OrderedDict

from django import forms
from employees.models.models_agreement import Agreement
from employees.validators.validators_agreement import (
    validate_create_date_not_after_start_date,
)
from orders.validators import (
    validate_end_date_after_start_date,
    validate_file_extension,
    validate_max_size_file,
    validate_no_future_create_date,
)


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
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "user": forms.HiddenInput(),
            "scan": forms.FileInput(),
        }
        labels = {
            "user": "",
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get("instance", None)
        user = kwargs.pop("user", None)
        if instance:
            initial_user_display = (
                f"{instance.user.first_name} {instance.user.last_name}"
            )
        else:
            initial_user_display = f"{user.first_name} {user.last_name}"
        super().__init__(*args, **kwargs)
        self.fields["user"].initial = user
        self.fields["user_display"].initial = initial_user_display

    def clean(self):
        cleaned_data = super().clean()
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        validate_no_future_create_date(cleaned_data=cleaned_data)
        validate_create_date_not_after_start_date(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        return cleaned_data
