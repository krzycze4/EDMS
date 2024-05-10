import django_filters
from django.contrib.auth import get_user_model
from employees.models.models_salaries import Salary

User = get_user_model()


class UserFilterSet(django_filters.FilterSet):
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


class SalaryFilterSet(django_filters.FilterSet):
    user_first_name = django_filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")
    user_last_name = django_filters.CharFilter(field_name="user__last_name", lookup_expr="icontains")

    class Meta:
        model = Salary
        fields = {
            "date": ["gte", "lte"],
            "fee": ["gte", "lte"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.form.fields.items():
            field.widget.attrs.update({"class": "form-control"})
