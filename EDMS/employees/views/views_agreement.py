from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_agreement import AgreementForm
from employees.models.models_agreement import Agreement

User = get_user_model()


class AgreementCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "employees.add_agreement"
    model = Agreement
    form_class = AgreementForm
    template_name = "employees/agreements/agreement_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        return kwargs


class AgreementDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "employees.view_agreement"
    model = Agreement
    template_name = "employees/agreements/agreement_detail.html"


class AgreementUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "employees.change_agreement"
    model = Agreement
    form_class = AgreementForm
    template_name = "employees/agreements/agreement_update.html"

    def get_success_url(self):
        return reverse("detail-agreement", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_scan"] = self.object.scan
        return context


class AgreementDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "employees.delete_agreement"
    model = Agreement
    template_name = "employees/agreements/agreement_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.object.user.pk})
