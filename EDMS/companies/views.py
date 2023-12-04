import os
from http import HTTPStatus

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, TemplateView
from requests import Timeout

from .forms import CompanyAndAddressForm, KRSForm
from .models import Address, Company


class FindCompanyView(FormView):
    template_name = "companies/find_company.html"
    form_class = KRSForm
    success_url = reverse_lazy("create_company")

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            krs = form.cleaned_data["krs_id"]
            api_url = os.path.join(settings.BASE_KRS_API_URL, krs)

            try:
                response = requests.get(url=api_url, timeout=settings.KRS_API_TIMEOUT)
            except Timeout:
                messages.error(
                    self.request,
                    message="Time limit for KRS request expired!",
                )
                return render(self.request, self.template_name, {"form": form})
            return self.handle_api_response(krs=krs, form=form, response=response)

    def handle_api_response(self, krs, form, response):
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

    def process_valid_response(self, response, krs):
        api_json = response.json()

        company_data = api_json["odpis"]["dane"]["dzial1"]["danePodmiotu"]
        name = company_data["nazwa"]
        regon = company_data["identyfikatory"]["regon"]
        nip = company_data["identyfikatory"]["nip"]

        company_address = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"]
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
        return redirect("create_company")


class CreateCompanyView(FormView):
    template_name = "companies/create_company.html"
    fields = "__all__"
    form_class = CompanyAndAddressForm
    success_url = reverse_lazy("create_company_done")

    def get_initial(self):
        initial = super().get_initial()
        company_data = self.request.session.get("company_data", {})
        initial.update(company_data)
        return initial

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        krs = form.cleaned_data["krs"]
        regon = form.cleaned_data["regon"]
        nip = form.cleaned_data["nip"]
        street_name = form.cleaned_data["street_name"]
        street_number = form.cleaned_data["street_number"]
        city = form.cleaned_data["city"]
        postcode = form.cleaned_data["postcode"]
        country = form.cleaned_data["country"]

        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )

        Company.objects.create(
            name=name, krs=krs, regon=regon, nip=nip, address=address
        )

        return super().form_valid(form)


class CreateCompanyDoneView(TemplateView):
    template_name = "companies/create_company_done.html"


class ListCompanyView(ListView):
    queryset = Company.objects.all()
    template_name = "companies/list_company.html"
    paginate_by = 2
    context_object_name = "companies"


class DetailCompanyView(DetailView):
    model = Company
    template_name = "companies/detail_company.html"
