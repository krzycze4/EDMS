from django import forms
from employees.models.models_payment import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["date", "user", "fee"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "user": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "fee": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {"user": "Employee"}
