import django_filters

from .models import Contract


class ContractFilterSet(django_filters.FilterSet):
    company_name = django_filters.CharFilter(
        field_name="company__name", lookup_expr="icontains"
    )

    class Meta:
        model = Contract
        fields = {
            "name": ["exact"],
            "create_date": ["gte", "lte"],
            "start_date": ["gte", "lte"],
            "end_date": ["gte", "lte"],
            "price": ["gte", "lte"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.form.fields.items():
            field.widget.attrs.update({"class": "form-control"})
