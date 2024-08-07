from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class CompanyListTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "companies/companies/list_company.html"

    def setUp(self) -> None:
        super().setUp()
        self.company_list = CompanyFactory.create_batch(11)

    def test_get_redirects_to_login(self):
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('list-company')}")

    def test_get_page_1_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_page_2_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")

    def test_get_page_1_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_page_2_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")

    def test_get_page_1_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_page_2_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")

    def test_get_page_1_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_page_2_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")
