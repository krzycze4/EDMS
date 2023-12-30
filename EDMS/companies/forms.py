from companies.models import Address, Company, Contact
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

    class Meta:
        fields = "__all__"


class UpdateCompanyIdentifiersForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "krs", "regon", "nip"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "street_number", "city", "postcode", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "description", "company"]
        widgets = {"company": forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UpdateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "description", "company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class DeleteContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "description", "company"]
