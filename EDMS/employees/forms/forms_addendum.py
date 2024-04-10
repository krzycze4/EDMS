from django import forms
from employees.models.models_addendum import Addendum
from employees.models.models_agreement import Agreement
from employees.validators.validators_addendum import validate_addendum_dates


class AddendumForm(forms.ModelForm):
    class Meta:
        model = Addendum
        fields = [
            "name",
            "create_date",
            "agreement",
            "end_date",
            "salary_gross",
            "scan",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "agreement": forms.Select(attrs={"class": "form-control js-example-basic-single"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "salary_gross": forms.NumberInput(attrs={"class": "form-control"}),
            "scan": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["agreement"].disabled = True
        self.fields["agreement"].queryset = Agreement.objects.exclude(termination__isnull=False)

    def clean(self):
        cleaned_data = super().clean()
        validate_addendum_dates(cleaned_data=cleaned_data)
        return cleaned_data
