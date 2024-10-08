from typing import Any, Dict, List, Union

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from invoices.models import Invoice
from orders.filters import OrderFilter
from orders.forms.forms_manage_invoices import ManageInvoicesForm
from orders.forms.forms_order import OrderCreateForm, OrderUpdateForm
from orders.models import Order


class OrderCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "orders.add_order"
    template_name = "orders/orders/create_order.html"
    form_class = OrderCreateForm

    def form_valid(self, form: OrderCreateForm) -> HttpResponse:
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})


class OrderDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "orders.view_order"
    template_name = "orders/orders/detail_order.html"
    model = Order

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        income_invoices = self.object.income_invoice.select_related("linked_invoice")
        context["income_invoices"] = income_invoices

        cost_invoices = self.object.cost_invoice.select_related("linked_invoice")
        context["cost_invoices"] = cost_invoices

        income_invoices_net_price_sum = self.count_invoices_sum(income_invoices)
        context["income_invoices_net_price_sum"] = income_invoices_net_price_sum

        cost_invoices_net_price_sum = self.count_invoices_sum(cost_invoices)
        context["cost_invoices_net_price_sum"] = cost_invoices_net_price_sum

        order_balance = income_invoices_net_price_sum - cost_invoices_net_price_sum
        context["order_balance"] = order_balance

        protocols = self.object.protocols.select_related("user").all()
        context["protocols"] = protocols

        context["contract"] = self.object.contract
        return context

    @staticmethod
    def count_invoices_sum(invoices: List[Union[Invoice | None]]) -> int:
        """
        Calculates the total net price of a list of invoices.

        Args:
            invoices (List[Union[Invoice | None]]): A list of invoices to calculate the sum from.

        Returns:
            int: The total net price after considering invoice types and linked invoices.
        """
        sum_net_price = 0
        for invoice in invoices:
            if invoice.type in [Invoice.ORIGINAL, Invoice.DUPLICATE] and invoice.linked_invoice is None:
                sum_net_price += invoice.net_price
            elif invoice.type == Invoice.CORRECTING:
                sum_net_price -= invoice.linked_invoice.net_price
                sum_net_price += invoice.net_price
        return sum_net_price


class OrderUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "orders.change_order"
    template_name = "orders/orders/update_order.html"
    model = Order
    form_class = OrderUpdateForm

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})


class OrderListView(PermissionRequiredMixin, ListView, LoginRequiredMixin):
    permission_required = "orders.view_order"
    template_name = "orders/orders/list_order.html"
    queryset = Order.objects.get_queryset().order_by("id")
    paginate_by = 10
    context_object_name = "orders"
    filter = None
    ordering = ["create_date"]

    def get_queryset(self) -> QuerySet:
        """
        Retrieves the list of orders from the database, filtered and ordered.

        Returns:
            QuerySet: The filtered and ordered list of orders.
        """
        queryset = super().get_queryset()
        self.filter = OrderFilter(self.request.GET, queryset=self.queryset)
        queryset = self.filter.qs
        queryset = queryset.select_related("user")
        queryset = queryset.select_related("company")
        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.filter.form
        return context


class OrderDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "orders.delete_order"
    template_name = "orders/orders/delete_order.html"
    model = Order
    success_url = reverse_lazy("list-order")


class OrderManageInvoices(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "orders.change_order"
    template_name = "orders/orders/manage_invoice.html"
    form_class = ManageInvoicesForm
    model = Order

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})
