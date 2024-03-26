from typing import Any, Dict, List, Union

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from invoices.filters import InvoiceFilter
from invoices.forms import InvoiceForm
from invoices.models import Invoice
from orders.models import Order


class InvoiceCreateView(CreateView, LoginRequiredMixin):
    template_name = "invoices/create_invoice.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse_lazy("detail-invoice", kwargs={"pk": self.object.pk})


class InvoiceDetailView(DetailView, LoginRequiredMixin):
    template_name = "invoices/detail_invoice.html"
    model = Invoice

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["child_invoices"] = self.get_child_invoices()
        return context

    def get_child_invoices(self) -> Union[List[Invoice] | str]:
        child_invoices = None
        if self.object.type in [Invoice.ORIGINAL, Invoice.DUPLICATE]:
            child_invoices = Invoice.objects.filter(linked_invoice=self.object)
        return child_invoices


class InvoiceListView(ListView, LoginRequiredMixin):
    template_name = "invoices/list_invoice.html"
    queryset = Invoice.objects.all()
    paginate_by = 10
    context_object_name = "invoices"
    filter = None
    ordering = ["create_date"]

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        self.filter = InvoiceFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filter.form
        return context


class InvoiceUpdateView(UpdateView, LoginRequiredMixin):
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


class InvoiceDeleteView(DeleteView, LoginRequiredMixin):
    model = Invoice
    template_name = "invoices/delete_invoice.html"
    success_url = reverse_lazy("list-invoice")
