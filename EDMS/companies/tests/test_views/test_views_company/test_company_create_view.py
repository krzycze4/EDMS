from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from companies.models import Address, Company
from companies.views.views_company import CompanyCreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class CompanyCreateTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        company = CompanyFactory.build()
        cls.company_session_data = {
            "name": company.name,
            "krs": company.krs,
            "regon": company.regon,
            "nip": company.nip,
            "street_name": company.address.street_name,
            "street_number": company.address.street_number,
            "city": company.address.city,
            "postcode": company.address.postcode,
            "country": company.address.country,
            "shortcut": company.shortcut,
        }
        cls.template_name = "companies/companies/create_company.html"

    def setUp(self) -> None:
        self.company = CompanyFactory.build()
        session = self.client.session
        session["company_data"] = self.company_session_data
        session.save()

    def test_redirect_to_login_on_get(self):
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('create-company')}")

    def test_redirect_to_login_on_post(self):
        response = self.client.post(reverse_lazy("create-company"), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('create-company')}")

    def test_initial_data_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        view = CompanyCreateView()
        view.request = response.wsgi_request
        initial = view.get_initial()
        self.assertEqual(initial, self.company_session_data)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_access_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_post_creates_company_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        company_counter = Company.objects.count()
        address_counter = Address.objects.count()
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Company.objects.count(), company_counter + 1)
        self.assertEqual(Address.objects.count(), address_counter + 1)
        self.assertRedirects(response, reverse_lazy("create-company-done"))

    def test_initial_data_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        view = CompanyCreateView()
        view.request = response.wsgi_request
        initial = view.get_initial()
        self.assertEqual(initial, self.company_session_data)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_access_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_post_creates_company_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        company_counter = Company.objects.count()
        address_counter = Address.objects.count()
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Company.objects.count(), company_counter + 1)
        self.assertEqual(Address.objects.count(), address_counter + 1)
        self.assertRedirects(response, reverse_lazy("create-company-done"))

    def test_get_access_denied_for_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_access_denied_for_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_access_denied_for_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_access_denied_for_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
