from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_agreement import AgreementForm
from employees.models.models_agreement import Agreement


class AgreementCreateView(CreateView):
    model = Agreement
    form_class = AgreementForm
    template_name = "users/agreements/agreement_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = get_user_model().objects.get(pk=self.kwargs["pk"])
        return kwargs


class AgreementDetailView(DetailView):
    model = Agreement
    template_name = "users/agreements/agreement_detail.html"


class AgreementUpdateView(UpdateView):
    model = Agreement
    form_class = AgreementForm
    template_name = "users/agreements/agreement_update.html"

    def get_success_url(self):
        return reverse("detail-agreement", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_scan"] = self.object.scan
        return context


class AgreementDeleteView(DeleteView):
    model = Agreement
    template_name = "users/agreements/agreement_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.object.user.pk})
