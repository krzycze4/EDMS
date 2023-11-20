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
    KRS_id = forms.IntegerField(
        label="KRS number",
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    REGON_id = forms.IntegerField(
        label="REGON number",
        widget=forms.TextInput(attrs={"readonly": "readonly", "class": "form-control"}),
    )
    NIP_id = forms.IntegerField(
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
