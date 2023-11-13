from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import User


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs["autofocus"] = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                message=f"Email '{email}' has been already used."
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    # PROBLEM
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
