from typing import Any, Dict

from contracts.filters import ContractFilterSet
from contracts.forms import ContractForm
from contracts.models import Contract
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class ContractCreateView(CreateView, LoginRequiredMixin):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-contract", kwargs={"pk": self.object.pk})


class ContractDetailView(DetailView, LoginRequiredMixin):
    model = Contract
    template_name = "contracts/contract_detail.html"


class ContractUpdateView(UpdateView, LoginRequiredMixin):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-contract", kwargs={"pk": self.object.pk})


class ContractDeleteView(DeleteView, LoginRequiredMixin):
    model = Contract
    template_name = "contracts/contract_delete.html"

    def get_success_url(self) -> str:
        return reverse("list-contract")


class ContractListView(ListView, LoginRequiredMixin):
    model = Contract
    template_name = "contracts/contract_list.html"
    paginate_by = 10
    filter_set = None
    ordering = "-create_date"
    context_object_name = "contracts"

    def get_queryset(self) -> QuerySet[Contract]:
        queryset = super().get_queryset()
        self.filter_set = ContractFilterSet(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
