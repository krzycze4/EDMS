from collections import OrderedDict

from companies.models import Address
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from orders.validators import end_after_start_validator, forbidden_future_date_validator

from .models import Agreement, User
from .validators import create_date_before_or_the_same_as_start_date


class CustomUserCreationForm(BaseUserCreationForm):
    first_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control form-control-user",
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Last Name",
            }
        ),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Email Address",
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-user", "placeholder": "Password"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Repeat Password",
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        field_classes = {"email": EmailField}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs["autofocus"] = True

    def clean_email(self) -> str:
        email: str = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                message=f"Email '{email}' has been already used."
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control form-control-user",
                "placeholder": "Enter Email Address",
            }
        ),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control form-control-user",
                "placeholder": "Password",
            }
        ),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "autofocus": True,
                "type": "email",
                "class": "form-control form-control-user",
                "id": "exampleInputEmail",
                "aria-describedby": "emailHelp",
                "placeholder": "Enter Email Address...",
            }
        ),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control form-control-user",
                "placeholder": "New Password",
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control form-control-user",
                "placeholder": "Confirm New Password",
            }
        ),
    )


class UserContactUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "position",
            "vacation_days",
            "photo",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "vacation_days": forms.NumberInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "custom-file", "type": "file"}),
        }


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


class UserAgreementCreateForm(forms.ModelForm):
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
                ("is_current", "is_current"),
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
            "is_current": forms.CheckboxInput(),
        }
        labels = {
            "user": "",
        }

    def __init__(self, *args, **kwargs):
        user_pk = kwargs.pop("pk")
        super().__init__(*args, **kwargs)
        user = User.objects.get(pk=user_pk)
        self.fields["user"].initial = user
        self.fields["user_display"].initial = f"{user.first_name} {user.last_name}"

    def clean(self):
        cleaned_data = super().clean()
        end_after_start_validator(cleaned_data=cleaned_data)
        forbidden_future_date_validator(cleaned_data=cleaned_data)
        create_date_before_or_the_same_as_start_date(cleaned_data=cleaned_data)
        return cleaned_data


class UserAgreementUpdateForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = [
            "name",
            "type",
            "salary_gross",
            "create_date",
            "start_date",
            "end_date",
            "scan",
            "is_current",
            "user",
        ]
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
            "scan": forms.FileInput(),
            "is_current": forms.CheckboxInput(),
            "user": forms.HiddenInput(),
        }
        labels = {"user": ""}

    def clean(self):
        cleaned_data = super().clean()
        end_after_start_validator(cleaned_data=cleaned_data)
        forbidden_future_date_validator(cleaned_data=cleaned_data)
        create_date_before_or_the_same_as_start_date(cleaned_data=cleaned_data)
        return cleaned_data
