from typing import Any, Dict, Union

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
from orders.filters import OrderFilter
from orders.forms import OrderCreateForm, OrderManageInvoicesForm, OrderUpdateForm
from orders.models import Order


class OrderCreateView(CreateView):
    template_name = "orders/orders/create_order.html"
    form_class = OrderCreateForm

    def form_valid(self, form: OrderCreateForm) -> HttpResponse:
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})


class OrderDetailView(DetailView):
    template_name = "orders/orders/detail_order.html"
    model = Order

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cost_invoices_net_price_sum = self.count_cost_invoices_sum()
        order_balance = self.count_order_balance(
            cost_invoices_net_price=cost_invoices_net_price_sum
        )
        context["cost_invoices_net_price_sum"] = cost_invoices_net_price_sum
        context["order_balance"] = order_balance
        return context

    def count_cost_invoices_sum(self) -> int:
        cost_invoices_net_price = 0
        for cost_invoice in self.object.cost_invoices.all():
            cost_invoices_net_price += cost_invoice.net_price
        return cost_invoices_net_price

    def count_order_balance(self, cost_invoices_net_price: Union[int | None]) -> int:
        order_balance = 0
        if cost_invoices_net_price:
            income_invoice_net_price = self.object.income_invoice.net_price
            order_balance = income_invoice_net_price - cost_invoices_net_price
        return order_balance


class OrderUpdateView(UpdateView):
    template_name = "orders/orders/update_order.html"
    model = Order
    form_class = OrderUpdateForm

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})


class OrderListView(ListView):
    template_name = "orders/orders/list_order.html"
    queryset = Order.objects.all()
    paginate_by = 10
    context_object_name = "orders"
    filter = None

    def get_queryset(self) -> QuerySet:
        self.filter = OrderFilter(self.request.GET, queryset=self.queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.filter.form
        return context


class OrderDeleteView(DeleteView):
    template_name = "orders/orders/delete_order.html"
    model = Order
    success_url = reverse_lazy("list-order")


class OrderManageInvoices(UpdateView):
    template_name = "orders/orders/manage_invoice.html"
    form_class = OrderManageInvoicesForm
    model = Order

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.pk})
