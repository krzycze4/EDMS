from typing import Any, Dict

from companies.models import Address
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from users.forms import (
    AddressForm,
    UserAgreementCreateForm,
    UserAgreementUpdateForm,
    UserContactUpdateForm,
)
from users.models import Agreement, User


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agreements"] = Agreement.objects.filter(user=self.object)
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserContactUpdateForm
    template_name = "users/user_update.html"

    def get_success_url(self):
        return reverse("detail-user", kwargs={"pk": self.object.pk})


class UserAddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = "users/user_address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form: AddressForm):
        street_name: str = form.cleaned_data["street_name"]
        street_number: str = form.cleaned_data["street_number"]
        city: str = form.cleaned_data["city"]
        postcode: str = form.cleaned_data["postcode"]
        country: str = form.cleaned_data["country"]
        user = User.objects.get(pk=self.kwargs["pk"])
        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )
        user.address = address
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class UserAddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "users/user_address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs["pk"])
        return Address.objects.get(pk=user.address.pk)

    def form_valid(self, form):
        street_name: str = form.cleaned_data["street_name"]
        street_number: str = form.cleaned_data["street_number"]
        city: str = form.cleaned_data["city"]
        postcode: str = form.cleaned_data["postcode"]
        country: str = form.cleaned_data["country"]
        user = User.objects.get(pk=self.kwargs["pk"])
        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )
        if User.objects.filter(address=user.address).count() == 1:
            user.address.delete()
        user.address = address
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class UserAgreementCreateView(CreateView):
    model = Agreement
    form_class = UserAgreementCreateForm
    template_name = "users/agreement_create.html"

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
    template_name = "users/agreement_detail.html"


class UserAgreementUpdateView(UpdateView):
    model = Agreement
    form_class = UserAgreementUpdateForm
    template_name = "users/agreement_update.html"

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
    template_name = "users/agreement_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.object.user.pk})
