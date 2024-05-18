from http import HTTPStatus
from typing import List

from companies.factories import AddressFactory
from companies.models import Address
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory


class TestCaseAddressModelViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        group_names_with_permission_codenames = {
            "ceos": [
                "add_company",
                "change_company",
                "delete_company",
                "view_company",
                "add_contact",
                "change_contact",
                "delete_contact",
                "add_address",
                "change_address",
                "delete_address",
                "view_address",
            ],
            "accountants": [
                "add_company",
                "change_company",
                "delete_company",
                "view_company",
                "add_contact",
                "change_contact",
                "delete_contact",
                "add_address",
                "change_address",
                "delete_address",
                "view_address",
            ],
            "managers": ["view_company", "add_contact", "view_address"],
            "hrs": ["view_company", "add_contact", "view_address"],
        }
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            cls.create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

    @staticmethod
    def create_group_with_permissions(group_name: str, permission_codenames: List[str]) -> "Group":
        from django.contrib.auth.models import Group, Permission

        permissions = Permission.objects.filter(codename__in=permission_codenames)
        group, _ = Group.objects.get_or_create(name=group_name)
        group.permissions.add(*permissions)
        return group

    def setUp(self) -> None:
        self.client = APIClient()
        self.address_list = AddressFactory.create_batch(10)
        self.address = AddressFactory.build()
        self.address_data = {
            "street_name": self.address.street_name,
            "street_number": str(self.address.street_number),
            "city": self.address.city,
            "postcode": self.address.postcode,
            "country": self.address.country,
        }
        self.password = "testPassword123!"

        accountant_group = get_object_or_404(Group, name="accountants")
        ceo_group = get_object_or_404(Group, name="ceos")
        hr_group = get_object_or_404(Group, name="hrs")
        manager_group = get_object_or_404(Group, name="managers")

        self.accountant = UserFactory(is_active=True, password=self.password, address=self.address_list[1])
        self.accountant.groups.add(accountant_group)

        self.ceo = UserFactory(is_active=True, password=self.password, address=self.address_list[1])
        self.ceo.groups.add(ceo_group)

        self.hr = UserFactory(is_active=True, password=self.password, address=self.address_list[1])
        self.hr.groups.add(hr_group)

        self.manager = UserFactory(is_active=True, password=self.password, address=self.address_list[1])
        self.manager.groups.add(manager_group)

    """NOT AUTHENTICATED"""

    def test_get_list_address_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_detail_address_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_create_address_if_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_address_if_user_not_authenticated(self):
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_address_if_user_not_authenticated(self):
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    """ACCOUNTANTS"""

    def test_get_list_address_if_user_group_accountant(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_accountant(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_accountant(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), 11)

    def test_put_update_address_if_user_group_accountant(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), 10)

    def test_delete_address_if_user_group_accountant(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), 9)

    """CEOS"""

    def test_get_list_address_if_user_group_ceo(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_ceo(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_ceo(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), 11)

    def test_put_update_address_if_user_group_ceo(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), 10)

    def test_delete_address_if_user_group_ceo(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), 9)

    """HRS"""

    def test_get_list_address_if_user_group_hr(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_hr(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_hr(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_address_if_user_group_hr(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_address_if_user_group_hr(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    """MANAGERS"""

    def test_get_list_address_if_user_group_manager(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_manager(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_manager(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_address_if_user_group_manager(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_address_if_user_group_manager(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    """DIFFERENT"""

    def test_not_create_same_address(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertRaises(serializers.ValidationError)
