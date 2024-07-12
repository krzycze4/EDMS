from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from contracts.factories import ContractFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ContractListTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "contracts/contract_list.html"

    def setUp(self) -> None:
        super().setUp()
        self.contract_list = ContractFactory.create_batch(11)
        self.query_params = {
            "name": self.contract_list[0].name,
            "create_date__gte": "",
            "create_date__lte": "",
            "start_date__gte": "",
            "start_date__lte": "",
            "end_date__gte": "",
            "end_date__lte": "",
            "price__gte": "",
            "price__lte": "",
            "company_name": "",
        }

    def test_get_redirects_to_login(self):
        response = self.client.get(reverse_lazy("list-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('list-contract')}")

    def test_retrieve_page_1_of_list_for_accountants_when_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_retrieve_page_2_of_list_for_accountants_when_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-contract')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_contracts_from_list_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"), data=self.query_params)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")

    def test_retrieve_page_1_of_list_for_ceos_when_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_retrieve_page_2_of_list_for_ceos_when_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-contract')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_contracts_from_list_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"), data=self.query_params)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")

    def test_access_denied_for_hrs_when_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_retrieve_page_1_of_list_for_managers_when_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_retrieve_page_2_of_list_for_managers_when_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(f"{reverse_lazy('list-contract')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter_contracts_from_list_for_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("list-contract"), data=self.query_params)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["contracts"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")
