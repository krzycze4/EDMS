from typing import Any, Dict, Union

from django import forms
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from orders.models import Order

from .filters import InvoiceFilter
from .forms import InvoiceForm
from .models import Invoice


class InvoiceCreateView(CreateView):
    template_name = "invoices/create_invoice.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse_lazy("detail-invoice", kwargs={"pk": self.object.pk})


class InvoiceDetailView(DetailView):
    template_name = "invoices/detail_invoice.html"
    model = Invoice

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        order = self.get_order()
        context["order"] = order
        return context

    def get_order(self) -> Union[Order | None]:
        if self.object.seller.is_mine:
            order = Order.objects.filter(income_invoice=self.object).first()
        else:
            order = Order.objects.filter(cost_invoices=self.object).first()
        return order


class InvoiceListView(ListView):
    template_name = "invoices/list_invoice.html"
    queryset = Invoice.objects.all()
    paginate_by = 10
    context_object_name = "invoices"
    filter = None

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        self.filter = InvoiceFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filter.form
        return context


class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/update_invoice.html"

    def get_success_url(self) -> str:
        return reverse("detail-invoice", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        order = self.get_order()
        context["order"] = order
        return context

    def get_order(self) -> Union[Order, None]:
        if self.object.seller.is_mine:
            order = Order.objects.filter(income_invoice=self.object).first()
        else:
            order = Order.objects.filter(cost_invoices=self.object).first()
        return order

    def get_form(self, form_class=None) -> InvoiceForm:
        form = super().get_form(form_class)
        if self.get_order():
            form.fields["seller"].widget = forms.HiddenInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            )
            form.fields["seller"].label = ""
            form.fields["buyer"].widget = forms.HiddenInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            )
            form.fields["buyer"].label = ""
        return form


class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = "invoices/delete_invoice.html"
    success_url = reverse_lazy("list-invoice")
