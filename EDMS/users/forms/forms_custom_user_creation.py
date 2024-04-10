from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import BaseUserCreationForm
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Password"}),
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
            raise forms.ValidationError(message=f"Email '{email}' has been already used.")
        return email
