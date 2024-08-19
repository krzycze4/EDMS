from typing import Any, Dict, List, Optional

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class InvoiceCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "invoices.add_invoice"
    template_name = "invoices/create_invoice.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse_lazy("detail-invoice", kwargs={"pk": self.object.pk})


class InvoiceDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "invoices.view_invoice"
    template_name = "invoices/detail_invoice.html"
    model = Invoice

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["child_invoices"] = self.get_child_invoices()
        context["order_from_income_invoice"] = self.object.order_from_income_invoice.all()
        context["order_from_cost_invoice"] = self.object.order_from_cost_invoice.all()
        return context

    def get_child_invoices(self) -> Optional[List[Invoice]]:
        child_invoices = None
        if self.object.type in [Invoice.ORIGINAL, Invoice.DUPLICATE]:
            child_invoices = Invoice.objects.filter(linked_invoice=self.object)
        return child_invoices


class InvoiceListView(PermissionRequiredMixin, ListView, LoginRequiredMixin):
    permission_required = "invoices.view_invoice"
    template_name = "invoices/list_invoice.html"
    queryset = Invoice.objects.all()
    paginate_by = 10
    context_object_name = "invoices"
    filter = None
    ordering = ["create_date"]

    def get_queryset(self) -> QuerySet[Invoice]:
        queryset: QuerySet = super().get_queryset()
        self.filter = InvoiceFilter(self.request.GET, queryset=queryset)
        queryset = self.filter.qs.select_related("seller", "buyer")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.filter.form
        return context


class InvoiceUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "invoices.change_invoice"
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/update_invoice.html"

    def get_success_url(self) -> str:
        return reverse("detail-invoice", kwargs={"pk": self.object.pk})

    def get_order(self) -> Order:
        if self.object.seller.is_mine:
            order = Order.objects.filter(income_invoice=self.object).first()
        else:
            order = Order.objects.filter(cost_invoice=self.object).first()
        return order

    def get_form(self, form_class=None) -> InvoiceForm:
        form = super().get_form(form_class)
        if self.get_order():
            form.fields["seller"].widget = forms.HiddenInput(attrs={"class": "form-control", "readonly": "readonly"})
            form.fields["seller"].label = ""
            form.fields["buyer"].widget = forms.HiddenInput(attrs={"class": "form-control", "readonly": "readonly"})
            form.fields["buyer"].label = ""
        return form


class InvoiceDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "invoices.delete_invoice"
    model = Invoice
    template_name = "invoices/delete_invoice.html"
    success_url = reverse_lazy("list-invoice")
