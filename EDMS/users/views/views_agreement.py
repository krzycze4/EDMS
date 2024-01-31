from typing import Any, Dict

from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from users.forms import UserAgreementCreateForm, UserAgreementUpdateForm
from users.models import Agreement


class UserAgreementCreateView(CreateView):
    model = Agreement
    form_class = UserAgreementCreateForm
    template_name = "users/agreements/agreement_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["pk"] = self.kwargs["pk"]
        return kwargs

    def form_valid(self, form) -> HttpResponse:
        is_current = form.cleaned_data["is_current"]
        user = form.cleaned_data["user"]
        if is_current:
            old_agreements = Agreement.objects.filter(user=user)
            for old_agreement in old_agreements:
                old_agreement.is_current = False
                old_agreement.save()
        return super().form_valid(form)


class UserAgreementDetailView(DetailView):
    model = Agreement
    template_name = "users/agreements/agreement_detail.html"


class UserAgreementUpdateView(UpdateView):
    model = Agreement
    form_class = UserAgreementUpdateForm
    template_name = "users/agreements/agreement_update.html"

    def get_success_url(self):
        return reverse("detail-user", kwargs={"pk": self.object.user.pk})

    def form_valid(self, form) -> HttpResponse:
        is_current = form.cleaned_data["is_current"]
        user = form.cleaned_data["user"]
        if is_current:
            old_agreements = Agreement.objects.filter(user=user)
            for old_agreement in old_agreements:
                old_agreement.is_current = False
                old_agreement.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_scan"] = self.object.scan
        return context


class UserAgreementDeleteView(DeleteView):
    model = Agreement
    template_name = "users/agreements/agreement_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.object.user.pk})
