from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class BaseContractModelViewSetTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.company = CompanyFactory.create()
        cls.employee = UserFactory.create()

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.contract_list = ContractFactory.create_batch(9, company=self.company)
        self.contract = ContractFactory.build(company=self.company)
        self.contract_data = {
            "name": self.contract.name,
            "create_date": self.contract.create_date,
            "start_date": self.contract.start_date,
            "end_date": self.contract.end_date,
            "company": self.contract.company.id,
            "employee": [self.employee.id],
            "price": [self.contract.price],
            "scan": self.contract.scan,
        }


class NotAuthenticatedUserContractModelViewSetTests(BaseContractModelViewSetTestCase):
    def test_unauthenticated_user_cannot_view_contract_list(self):
        response = self.client.get(reverse_lazy("contract-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_contract_detail(self):
        response = self.client.get(reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_contract(self):
        response = self.client.post(reverse_lazy("contract-list"), self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_contract(self):
        response = self.client.put(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_contract(self):
        response = self.client.delete(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class AccountantsContractModelViewSetTests(BaseContractModelViewSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_accountant_can_view_contract_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_contract_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_contract(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contract-list"), self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), 9)

    def test_accountant_cannot_update_contract(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(Contract.objects.get(id=self.contract_list[0].id).name == self.contract_data["name"])

    def test_accountant_cannot_delete_contract(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), 9)


class CeosContractModelViewSetTests(BaseContractModelViewSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_ceo_can_view_contract_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_contract_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_contract(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contract-list"), self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contract.objects.count(), 10)

    def test_ceo_can_update_contract(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Contract.objects.get(id=self.contract_list[0].id).name == self.contract_data["name"])

    def test_ceo_can_delete_contract(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contract.objects.count(), 8)


class HrsContractModelViewSetTests(BaseContractModelViewSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.hr = self.create_user_with_group(group_name="hrs")
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_hr_cannot_view_contract_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_hr_cannot_view_contract_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_hr_cannot_create_contract(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contract-list"), self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_hr_cannot_update_contract(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(Contract.objects.get(id=self.contract_list[0].id).name == self.contract_data["name"])

    def test_hr_cannot_delete_contract(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), 9)


class ManagersContractModelViewSetTests(BaseContractModelViewSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.hr = self.create_user_with_group(group_name="hrs")
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_manager_cannot_view_contract_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_view_contract_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_contract(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contract-list"), self.contract_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_cannot_update_contract(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertFalse(Contract.objects.get(id=self.contract_list[0].id).name == self.contract_data["name"])

    def test_manager_cannot_delete_contract(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contract-detail", kwargs={"pk": self.contract_list[0].id}), self.contract_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), 9)
