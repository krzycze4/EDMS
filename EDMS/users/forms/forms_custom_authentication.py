from django import forms
from django.contrib.auth.forms import AuthenticationForm


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
