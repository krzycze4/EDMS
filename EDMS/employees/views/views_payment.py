from typing import Any, Dict

from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from employees.filters import PaymentFilterSet
from employees.forms.forms_payment import PaymentForm
from employees.models.models_payment import Payment


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "employees/payments/payment_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-payment", kwargs={"pk": self.object.pk})


class PaymentDetailView(DetailView):
    model = Payment
    template_name = "employees/payments/payment_detail.html"


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "employees/payments/payment_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-payment", kwargs={"pk": self.object.pk})


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = "employees/payments/payment_delete.html"
    success_url = reverse_lazy("list-payment")


class PaymentListView(ListView):
    model = Payment
    ordering = "-date"
    paginate_by = 10
    template_name = "employees/payments/payment_list.html"
    filter_set = None
    context_object_name = "payments"

    def get_queryset(self) -> QuerySet[Payment]:
        self.filter_set = PaymentFilterSet(
            self.request.GET, queryset=Payment.objects.all()
        )
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
