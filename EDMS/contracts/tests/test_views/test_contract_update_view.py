from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from users.factories import UserFactory

User = get_user_model()


class ContractUpdateViewTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "contracts/contract_update.html"

    def setUp(self) -> None:
        super().setUp()
        self.contract = ContractFactory.create()
        company = CompanyFactory.create()
        employee = UserFactory.create()
        self.contract_stub = ContractFactory.stub(company=company, employee=employee)
        self.valid_contract_data = {
            "name": self.contract_stub.name,
            "create_date": self.contract_stub.create_date,
            "start_date": self.contract_stub.start_date,
            "end_date": self.contract_stub.end_date,
            "company": company.pk,
            "employee": employee.pk,
            "price": self.contract_stub.price,
            "scan": self.contract_stub.scan,
        }
        self.invalid_contract_data = {
            "name": self.contract_stub.name,
            "create_date": self.contract_stub.create_date,
            "start_date": self.contract_stub.start_date,
            "end_date": self.contract_stub.end_date,
            "company": company.pk,
            "employee": employee.pk,
            "price": -1,
        }
        self.not_logged_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('update-contract', kwargs={'pk': self.contract.pk})}"
        )
        self.success_redirect_url = f"{reverse_lazy('detail-contract', kwargs={'pk': self.contract.pk})}"

    def test_get_redirects_to_login(self):
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_post_redirects_to_login(self):
        response = self.client.post(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_get_accountants_access_forbidden(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_accountants_updates_forbidden(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data=self.valid_contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_ceos_access_ok(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_ceos_access_not_found(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        not_existing_pk = Contract.objects.last().pk + 1
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": not_existing_pk}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_ceos_updates_company_ok(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data=self.valid_contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_redirect_url)
        self.assertEqual(Contract.objects.get(pk=self.contract.pk).name, self.valid_contract_data["name"])

    def test_post_ceos_validation_errors(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data=self.invalid_contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["form"].errors)

    def test_get_hrs_access_forbidden(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_hrs_updates_forbidden(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data=self.valid_contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_managers_access_forbidden(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_managers_updates_forbidden(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-contract", kwargs={"pk": self.contract.pk}), data=self.valid_contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
