from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import AddressFactory, CompanyFactory
from companies.models import Company
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient

User = get_user_model()


class BaseCompanyApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.address = AddressFactory.create()
        self.company = CompanyFactory.build(address=self.address)
        self.company_data = {
            "name": self.company.name,
            "krs": self.company.krs,
            "regon": self.company.regon,
            "nip": self.company.nip,
            "address": self.company.address.id,
            "is_mine": self.company.is_mine,
            "shortcut": self.company.shortcut,
        }
        self.company_list = CompanyFactory.create_batch(10, address=self.address)


class UnauthenticatedUserApiCompanyTests(BaseCompanyApiTestCase):
    def test_unauthenticated_user_cannot_view_address_list(self):
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_address_detail(self):
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_address(self):
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_address(self):
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_address(self):
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class AccountantApiCompanyTests(BaseCompanyApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_accountant_can_view_company_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_company_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_create_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), count_company_before_response + 1)

    def test_accountant_can_update_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_accountant_can_delete_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.delete(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), count_company_before_response - 1)


class CeoApiCompanyTests(BaseCompanyApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_ceo_can_view_company_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_company_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), count_company_before_response + 1)

    def test_ceo_can_update_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_ceo_can_delete_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), count_company_before_response - 1)


class HrApiCompanyTests(BaseCompanyApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_hr_can_view_company_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_company_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_cannot_create_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_hr_cannot_update_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_hr_cannot_delete_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)


class ManagerApiCompanyTests(BaseCompanyApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_manager_can_view_company_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_company_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_manager_cannot_update_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)

    def test_manager_cannot_delete_company(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Company.objects.count(), count_company_before_response)


class CreateInstanceApiCompanyTests(BaseCompanyApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_prevent_duplicate_company_creation(self):
        self.assertTrue(self.login)
        count_company_before_response = Company.objects.count()
        self.client.post(reverse_lazy("company-list"), self.company_data)
        self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(Company.objects.count(), count_company_before_response + 1)
        self.assertRaises(serializers.ValidationError)
