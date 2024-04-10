from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class GroupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["groups"]
        widgets = {
            "groups": forms.SelectMultiple(attrs={"class": "form-control js-example-basic-multiple", "size": 4}),
        }
