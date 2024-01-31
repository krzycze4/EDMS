import django_filters
from users.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "first_name": ["icontains"],
            "last_name": ["icontains"],
            "email": ["icontains"],
            "phone_number": ["exact"],
            "position": ["exact"],
            "is_active": ["exact"],
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name, field in self.form.fields.items():
            field.widget.attrs.update({"class": "form-control"})
