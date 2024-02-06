from collections import OrderedDict
from typing import Any, Dict

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
from orders.validators import (
    validate_end_date_after_start_date,
    validate_file_extension,
    validate_max_size_file,
    validate_no_future_create_date,
)

from .models import Addendum, Agreement, Termination, User, Vacation
from .validators import (
    validate_addendum_dates,
    validate_create_date_not_after_start_date,
    validate_no_overlap_dates,
    validate_no_repetitions,
    validate_termination_dates,
)


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
            "photo",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
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


class AgreementForm(forms.ModelForm):
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
        }
        labels = {
            "user": "",
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get("instance", None)
        user = kwargs.pop("user", None)
        if instance:
            initial_user_display = (
                f"{instance.user.first_name} {instance.user.last_name}"
            )
        else:
            initial_user_display = f"{user.first_name} {user.last_name}"
        super().__init__(*args, **kwargs)
        self.fields["user"].initial = user
        self.fields["user_display"].initial = initial_user_display

    def clean(self):
        cleaned_data = super().clean()
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        validate_no_future_create_date(cleaned_data=cleaned_data)
        validate_create_date_not_after_start_date(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        return cleaned_data


class VacationForm(forms.ModelForm):
    leave_user_display = forms.CharField(
        label="Leave user",
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
    )

    class Meta:
        model = Vacation
        fields = [
            "type",
            "start_date",
            "end_date",
            "leave_user",
            "leave_user_display",
            "substitute_users",
            "scan",
        ]
        widgets = {
            # "id": forms.HiddenInput(),
            "type": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "end_date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "end_date"}
            ),
            "leave_user": forms.HiddenInput(),
            "substitute_users": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 3}
            ),
            "scan": forms.FileInput(),
        }
        labels = {
            "id": "",
            "leave_user": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["substitute_users"].queryset = User.objects.exclude(
            pk=kwargs["initial"]["leave_user"]
        )

    def clean(self) -> Dict[str, Any]:
        cleaned_data: Dict[str, Any] = super().clean()
        print(self.instance)
        if self.instance.pk:
            cleaned_data["id"] = self.instance.pk
        validate_end_date_after_start_date(cleaned_data=cleaned_data)
        validate_no_overlap_dates(cleaned_data=cleaned_data)
        validate_file_extension(cleaned_data=cleaned_data)
        validate_max_size_file(cleaned_data=cleaned_data)
        if not self.instance.pk:
            validate_no_repetitions(cleaned_data=cleaned_data)
        return cleaned_data


class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = ["name", "create_date", "agreement", "end_date", "scan"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "agreement": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "scan": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["agreement"].disabled = True
        else:
            self.fields["agreement"].queryset = Agreement.objects.filter(
                termination=None
            )

    def clean(self):
        cleaned_data = super().clean()
        validate_termination_dates(cleaned_data=cleaned_data)
        return cleaned_data


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
            "create_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "agreement": forms.Select(
                attrs={"class": "form-control js-example-basic-single"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "salary_gross": forms.NumberInput(attrs={"class": "form-control"}),
            "scan": forms.FileInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["agreement"].disabled = True
        self.fields["agreement"].queryset = Agreement.objects.exclude(
            termination__isnull=False
        )

    def clean(self):
        cleaned_data = super().clean()
        validate_addendum_dates(cleaned_data=cleaned_data)
        return cleaned_data
