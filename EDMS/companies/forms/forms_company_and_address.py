from companies.models import Address, Company
from django import forms


class KRSForm(forms.Form):
    krs_id = forms.CharField(
        label="Numer KRS",
        max_length=14,
        widget=forms.NumberInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "KRS number",
            }
        ),
    )


class CompanyAndAddressForm(forms.Form):
    name = forms.CharField(
        label="Company name",
        max_length=100,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    krs = forms.IntegerField(
        label="KRS number",
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    regon = forms.IntegerField(
        label="REGON number",
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    nip = forms.IntegerField(
        label="NIP number",
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    street_name = forms.CharField(
        label="Street name",
        max_length=100,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    street_number = forms.CharField(
        label="Street number",
        max_length=10,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    postcode = forms.CharField(
        label="Postcode",
        max_length=10,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    country = forms.CharField(
        label="Country",
        max_length=50,
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    shortcut = forms.CharField(
        label="Shortcut",
        max_length=5,
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not Company.objects.filter(is_mine=True).exists():
            self.fields["is_mine"] = forms.BooleanField(
                label="That's my company: ",
                widget=forms.CheckboxInput(attrs={"class": "form-check-input ml-2"}),
                required=False,
            )


class UpdateCompanyIdentifiersForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "krs", "regon", "nip", "shortcut", "is_mine"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "is_mine":
                field.widget.attrs["class"] = "form-check-input ml-2"
            else:
                field.widget.attrs["class"] = "form-control"


class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "street_number", "city", "postcode", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
