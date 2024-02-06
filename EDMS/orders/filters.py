import django_filters
from django import forms
from users.models import User

from .models import Order


class OrderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Order name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    payment__gt = django_filters.NumberFilter(
        field_name="payment",
        label="Payment from",
        lookup_expr="gte",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    payment__lt = django_filters.NumberFilter(
        field_name="payment",
        label="Payment to",
        lookup_expr="lte",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    status = django_filters.ChoiceFilter(
        choices=Order.STATUS_CHOICES,
        label="Status",
        lookup_expr="exact",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Create by",
        lookup_expr="exact",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    create_date__gt = django_filters.DateFilter(
        field_name="create_date",
        label="Create end_date from",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
    )
    create_date__lt = django_filters.DateFilter(
        field_name="create_date",
        label="Create end_date to",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
    )
    start_date = django_filters.DateFilter(
        label="Start service end_date",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
    )
    end_date = django_filters.DateFilter(
        label="End service end_date",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "end_date"}),
    )

    class Meta:
        model = Order
        fields = [
            "name",
            "payment__gt",
            "payment__lt",
            "status",
            "user",
            "create_date__gt",
            "create_date__lt",
            "start_date",
            "end_date",
        ]
