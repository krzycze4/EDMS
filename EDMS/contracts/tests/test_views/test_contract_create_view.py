from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from users.factories import UserFactory

User = get_user_model()


class BaseContractCreateTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.contract = ContractFactory.create()
        company = CompanyFactory.create()
        employee = UserFactory.create()
        self.contract_stub = ContractFactory.stub(company=company)
        self.contract_data = {
            "name": self.contract_stub.name,
            "create_date": self.contract_stub.create_date,
            "start_date": self.contract_stub.start_date,
            "end_date": self.contract_stub.end_date,
            "company": company.pk,
            "employee": employee.pk,
            "price": self.contract_stub.price,
            "scan": self.contract_stub.scan,
        }
        self.not_logged_user_url = f"{reverse_lazy('login')}?next={reverse_lazy('create-contract')}"


class UserNotAuthenticatedContractCreateViewTests(BaseContractCreateTestCase):
    def test_redirect_to_login_on_get_when_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("create-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_on_post_when_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("create-contract"), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)


class AccountantsContractCreateViewTests(BaseContractCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_deny_render_create_contract_for_accountants_when_execute_get_method(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_contract_for_accountants_when_execute_post_method(self):
        self.assertTrue(self.login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("create-contract"), data=self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)


class CeosContractCreateViewTests(BaseContractCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_render_create_contract_for_ceos_when_execute_get_method(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-contract"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_contract_and_redirect_for_ceos_when_execute_post_method(self):
        self.assertTrue(self.login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("create-contract"), data=self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contract.objects.count(), contract_counter + 1)
        new_contact = Contract.objects.latest("pk")
        self.assertRedirects(response, reverse_lazy("detail-contract", kwargs={"pk": new_contact.pk}))


class HrsContractCreateViewTests(BaseContractCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_deny_render_create_contract_for_hrs_when_execute_get_method(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_contract_for_hrs_when_execute_post_method(self):
        self.assertTrue(self.login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("create-contract"), data=self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)


class ManagerContractCreateViewTests(BaseContractCreateTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_deny_render_create_contract_for_managers_when_execute_get_method(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-contract"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_contract_for_managers_when_execute_post_method(self):
        self.assertTrue(self.login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("create-contract"), data=self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)
