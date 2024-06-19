from datetime import date
from typing import Dict, List, Union

from django import forms
from django.core.files.uploadedfile import UploadedFile
from orders.models import Protocol
from orders.validators.validators_protocol import ProtocolValidator


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ["scan", "create_date"]
        widgets = {
            "scan": forms.FileInput(attrs={"type": "file"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean(self) -> Dict[str, Union[date | UploadedFile]]:
        cleaned_data: Dict[str, Union[date | UploadedFile]] = super().clean()
        validators: List[callable] = ProtocolValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
