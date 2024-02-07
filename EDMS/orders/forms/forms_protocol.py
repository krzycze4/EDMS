from typing import Any, Dict

from django import forms
from orders.models import Protocol
from orders.validators import (
    validate_file_extension,
    validate_max_size_file,
    validate_no_future_create_date,
)


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ["scan", "create_date"]
        widgets = {
            "scan": forms.FileInput(attrs={"type": "file"}),
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "end_date"}
            ),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        validate_no_future_create_date(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        return cleaned_data
