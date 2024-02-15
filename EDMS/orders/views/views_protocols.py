from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from orders.forms.forms_protocol import ProtocolForm
from orders.models import Order, Protocol


class ProtocolCreateView(CreateView, LoginRequiredMixin):
    template_name = "orders/protocols/create_protocol.html"
    form_class = ProtocolForm

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self) -> str:
        return reverse("create-protocol", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form: ProtocolForm) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.order = Order.objects.get(pk=self.kwargs["pk"])
        response = super().form_valid(form)
        return response


class ProtocolDeleteView(DeleteView, LoginRequiredMixin):
    template_name = "orders/protocols/delete_protocol.html"
    model = Protocol

    def get_success_url(self) -> str:
        return reverse("detail-order", kwargs={"pk": self.object.order.pk})
