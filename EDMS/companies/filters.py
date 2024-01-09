import django_filters
from companies.models import Company


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            "name": ["icontains"],
            "krs": ["exact"],
            "regon": ["exact"],
            "nip": ["exact"],
            "shortcut": ["icontains"],
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name, field in self.form.fields.items():
            field.widget.attrs.update({"class": "form-control"})
