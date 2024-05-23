import os
from http import HTTPStatus
from typing import Callable, Dict, Union

import requests
from companies.filters import CompanyFilter
from companies.forms.forms_company_and_address import (
    CompanyAndAddressForm,
    KRSForm,
    UpdateAddressForm,
    UpdateCompanyIdentifiersForm,
)
from companies.models import Address, Company
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)


class CompanyFindView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = "companies.add_company"
    template_name = "companies/companies/find_company.html"
    form_class = KRSForm
    success_url = reverse_lazy("create-company")

    def post(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse | Callable]:
        form: KRSForm = self.get_form()

        if form.is_valid():
            krs: str = form.cleaned_data["krs_id"]
            api_url: str = os.path.join(settings.BASE_KRS_API_URL, krs)

            try:
                response: requests.Response = requests.get(url=api_url, timeout=settings.KRS_API_TIMEOUT)
            except requests.Timeout:
                messages.error(
                    self.request,
                    message="Time limit for KRS request expired!",
                )
                return render(self.request, self.template_name, {"form": form})
            return self.handle_api_response(krs=krs, form=form, response=response)

    def handle_api_response(
        self, krs: str, form: KRSForm, response: requests.Response
    ) -> Union[HttpResponse | HttpResponseRedirect | Callable]:
        if Company.objects.filter(krs=krs).exists():
            messages.warning(
                self.request,
                message="Company has already existed in the system!",
            )
            return render(self.request, self.template_name, {"form": form})

        if response.status_code == HTTPStatus.OK:
            return self.process_valid_response(response=response, krs=krs)
        elif response.status_code == HTTPStatus.NOT_FOUND:
            messages.error(
                self.request,
                message="Company doesn't exist! Insert correct KRS number.",
            )
        return render(self.request, self.template_name, {"form": form})

    def process_valid_response(self, response: requests.Response, krs: str) -> HttpResponseRedirect:
        api_json = response.json()

        company_data: Dict[str, Union[str, Dict[str, str]]] = api_json["odpis"]["dane"]["dzial1"]["danePodmiotu"]
        name: str = company_data["nazwa"]
        regon: str = company_data["identyfikatory"]["regon"]
        nip: str = company_data["identyfikatory"]["nip"]

        company_address: Dict[str, Union[str, Dict[str, str]]] = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"][
            "adres"
        ]
        street_name = company_address["ulica"]
        street_number = company_address["nrDomu"]
        city = company_address["miejscowosc"]
        postcode = company_address["kodPocztowy"]
        country = company_address["kraj"]

        self.request.session["company_data"] = {
            "name": name,
            "krs": krs,
            "regon": regon,
            "nip": nip,
            "street_name": street_name,
            "street_number": street_number,
            "city": city,
            "postcode": postcode,
            "country": country,
        }
        return redirect("create-company")


class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = "companies.add_company"
    template_name = "companies/companies/create_company.html"
    form_class = CompanyAndAddressForm
    success_url = reverse_lazy("create-company-done")

    def get_initial(self) -> Dict[str, str]:
        initial = super().get_initial()
        company_data = self.request.session.get("company_data", {})
        initial.update(company_data)
        return initial

    def form_valid(self, form: CompanyAndAddressForm) -> HttpResponse:
        name: str = form.cleaned_data["name"]
        krs: int = form.cleaned_data["krs"]
        regon: int = form.cleaned_data["regon"]
        nip: int = form.cleaned_data["nip"]
        street_name: str = form.cleaned_data["street_name"]
        street_number: str = form.cleaned_data["street_number"]
        city: str = form.cleaned_data["city"]
        postcode: str = form.cleaned_data["postcode"]
        country: str = form.cleaned_data["country"]
        shortcut: str = form.cleaned_data["shortcut"]
        if not Company.objects.filter(is_mine=True).exists():
            is_mine: bool = form.cleaned_data["is_mine"]
        else:
            is_mine = False

        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )

        Company.objects.create(
            name=name,
            krs=krs,
            regon=regon,
            nip=nip,
            address=address,
            shortcut=shortcut,
            is_mine=is_mine,
        )

        return super().form_valid(form)


class CreateCompanyDoneView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = "companies.add_company"
    template_name = "companies/companies/create_company_done.html"


class CompanyListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "companies.view_company"
    queryset = Company.objects.all()
    template_name = "companies/companies/list_company.html"
    context_object_name = "companies"
    paginate_by = 10
    filter_set = None
    ordering = "shortcut"

    def get_queryset(self) -> QuerySet[Company]:
        queryset = super().get_queryset()
        self.filter_set = CompanyFilter(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_set.form
        return context


class CompanyDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "companies.view_company"
    model = Company
    template_name = "companies/companies/detail_company.html"


class CompanyIdentifiersUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "companies.change_company"
    model = Company
    form_class = UpdateCompanyIdentifiersForm
    template_name = "companies/companies/update_identifiers_company.html"

    def get_success_url(self):
        return reverse_lazy("detail-company", kwargs={"pk": self.object.pk})


class CompanyAddressUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "companies.change_company"
    model = Address
    form_class = UpdateAddressForm
    template_name = "companies/companies/update_address_company.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(pk=self.kwargs["pk"])
        context["company"] = company
        return context

    def get_success_url(self):
        return reverse_lazy("detail-company", kwargs={"pk": self.kwargs["pk"]})
