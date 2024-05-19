from http import HTTPStatus

from companies.factories import AddressFactory, CompanyFactory
from companies.models import Company
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseCompanyModelViewSetMixin:
    @classmethod
    def setUpTestData(cls):
        group_names_with_permission_codenames = {
            "ceos": [
                "add_company",
                "change_company",
                "delete_company",
                "view_company",
            ],
            "accountants": ["add_company", "change_company", "delete_company", "view_company", "add_address"],
            "managers": ["view_company"],
            "hrs": ["view_company"],
        }
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

        cls.password = "testPassword123!"
        cls.user_address = AddressFactory.create()

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password, address=cls.user_address)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.client = APIClient()
        self.address = AddressFactory.create()
        self.company_list = CompanyFactory.create_batch(10, address=self.address)
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


class TestCaseUserNotAuthenticated(TestCaseCompanyModelViewSetMixin, TestCase):
    def test_get_list_company_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_detail_company_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_create_company_if_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_company_if_user_not_authenticated(self):
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_company_if_user_not_authenticated(self):
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseUserAccountant(TestCaseCompanyModelViewSetMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.accountant = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_list_company_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_company_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_company_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), 11)

    def test_put_update_company_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), 10)

    def test_delete_company_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), 9)


class TestCaseUserCeo(TestCaseCompanyModelViewSetMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_list_company_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_company_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_company_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), 11)

    def test_put_update_company_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), 10)

    def test_delete_company_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), 9)


class TestCaseUserHr(TestCaseCompanyModelViewSetMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.hr = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_list_company_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_company_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_company_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), 11)

    def test_put_update_company_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), 10)

    def test_delete_company_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), 9)


class TestCaseUserManager(TestCaseCompanyModelViewSetMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.manager = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_list_company_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_company_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_company_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Company.objects.count(), 11)

    def test_put_update_company_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Company.objects.count(), 10)

    def test_delete_company_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("company-detail", kwargs={"pk": self.company_list[0].id}), self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Company.objects.count(), 9)


class TestCaseCreateInstance(TestCaseCompanyModelViewSetMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_not_create_same_company(self):
        self.assertTrue(self.login)
        self.client.post(reverse_lazy("company-list"), self.company_data)
        self.client.post(reverse_lazy("company-list"), self.company_data)
        self.assertRaises(serializers.ValidationError)
