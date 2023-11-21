import os

import requests
from django.conf import settings
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from requests import Timeout

from .forms import CompanyAndAddressForm, KRSForm
from .models import Address, Company


class DashboardView(TemplateView):
    template_name = "dashboards/dashboard.html"


class FindCompanyView(FormView):
    template_name = "dashboards/find_company.html"
    form_class = KRSForm
    success_url = reverse_lazy("create_company")

    def form_valid(self, form):
        KRS_id = form.cleaned_data["krs_id"]
        api_url = os.path.join(settings.BASE_KRS_API_URL, KRS_id)

        try:
            response = requests.get(url=api_url, timeout=settings.KRS_API_TIMEOUT)
        except Timeout:
            messages.error(
                self.request,
                message="Time limit for KRS request expired!",
            )
            return render(self.request, self.template_name, {"form": form})

        if Company.objects.filter(KRS_id=KRS_id).exists():
            messages.warning(
                self.request,
                message="Company has already existed in the system!",
            )
            return render(self.request, self.template_name, {"form": form})

        if response.status_code == 200:
            api_json = response.json()

            name = api_json["odpis"]["dane"]["dzial1"]["danePodmiotu"]["nazwa"]
            REGON_id = api_json["odpis"]["dane"]["dzial1"]["danePodmiotu"][
                "identyfikatory"
            ]["regon"]
            NIP_id = api_json["odpis"]["dane"]["dzial1"]["danePodmiotu"][
                "identyfikatory"
            ]["nip"]

            street_name = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"][
                "adres"
            ]["ulica"]
            street_number = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"][
                "adres"
            ]["nrDomu"]
            city = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"][
                "miejscowosc"
            ]
            postcode = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"][
                "kodPocztowy"
            ]
            country = api_json["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"][
                "kraj"
            ]

            self.request.session["company_data"] = {
                "name": name,
                "KRS_id": KRS_id,
                "REGON_id": REGON_id,
                "NIP_id": NIP_id,
                "street_name": street_name,
                "street_number": street_number,
                "city": city,
                "postcode": postcode,
                "country": country,
            }
            return redirect("create_company")
        elif response.status_code == 404:
            messages.error(
                self.request,
                message="Company doesn't exist! Insert correct KRS number.",
            )
            return render(self.request, self.template_name, {"form": form})


class CreateCompanyView(FormView):
    template_name = "dashboards/create_company.html"
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
        KRS_id = form.cleaned_data["KRS_id"]
        REGON_id = form.cleaned_data["REGON_id"]
        NIP_id = form.cleaned_data["NIP_id"]
        street_name = form.cleaned_data["street_name"]
        street_number = form.cleaned_data["street_number"]
        city = form.cleaned_data["city"]
        postcode = form.cleaned_data["postcode"]
        country = form.cleaned_data["country"]

        address = Address.objects.filter(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )

        if not address:
            address = Address.objects.create(
                street_name=street_name,
                street_number=street_number,
                city=city,
                postcode=postcode,
                country=country,
            )

        Company.objects.create(
            name=name, KRS_id=KRS_id, REGON_id=REGON_id, NIP_id=NIP_id, address=address
        )

        return super().form_valid(form)


class CreateCompanyDoneView(TemplateView):
    template_name = "dashboards/create_company_done.html"


class ListCompanyView(ListView):
    queryset = Company.objects.values("name", "KRS_id", "REGON_id", "NIP_id")
    template_name = "dashboards/list_company.html"
    paginate_by = 10
    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        desired_columns = ["name", "KRS_id", "REGON_id", "NIP_id"]
        columns = Company._meta.fields
        desired_columns_name = [
            column.verbose_name for column in columns if column.name in desired_columns
        ]
        context["columns_name"] = desired_columns_name
        return context
