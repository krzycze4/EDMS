from companies.models import Address
from django import forms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "street_number", "city", "postcode", "country"]
        widgets = {
            "street_name": forms.TextInput(attrs={"class": "form-control"}),
            "street_number": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postcode": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
