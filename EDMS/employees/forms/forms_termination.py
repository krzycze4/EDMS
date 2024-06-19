from datetime import date
from typing import Dict, List, Union

from django import forms
from django.core.files.uploadedfile import UploadedFile
from employees.models.models_agreement import Agreement
from employees.models.models_termination import Termination
from employees.validators.validators_termination import TerminationValidator


class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = ["name", "create_date", "agreement", "end_date", "scan"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "agreement": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "scan": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["agreement"].disabled = True
        else:
            self.fields["agreement"].queryset = Agreement.objects.filter(termination=None)

    def clean(self) -> Dict[str, Union[str | date | Agreement | UploadedFile]]:
        cleaned_data: Dict[str, Union[str | date | Agreement | UploadedFile]] = super().clean()
        validators: List[callable] = TerminationValidator.all_validators()
        for validator in validators:
            validator(cleaned_data=cleaned_data)
        return cleaned_data
