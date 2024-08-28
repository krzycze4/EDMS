import django_filters
from django import forms
from django.utils import timezone

from .models import Invoice


class InvoiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Invoice Name",
        lookup_expr="exact",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    seller__name = django_filters.CharFilter(
        lookup_expr="icontains", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    buyer__name = django_filters.CharFilter(
        lookup_expr="icontains", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    create_date__gt = django_filters.DateFilter(
        field_name="create_date",
        lookup_expr="gte",
        label="Date From",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "date"}),
    )
    create_date__lt = django_filters.DateFilter(
        field_name="create_date",
        lookup_expr="lte",
        label="Date To",
        widget=forms.TextInput(attrs={"class": "form-control", "type": "date"}),
    )
    unpaid = django_filters.BooleanFilter(
        label="Show only unpaid postponed invoices",
        method="filter_unpaid_postponed_invoices",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input ml-2"}),
    )

    class Meta:
        model = Invoice
        fields = [
            "name",
            "seller__name",
            "buyer__name",
            "create_date__gt",
            "create_date__lt",
        ]

    @staticmethod
    def filter_unpaid_postponed_invoices(queryset, name, value):
        if value:
            today = timezone.now().date()
            return queryset.filter(is_paid=False, payment_date__lt=today)
        return queryset
