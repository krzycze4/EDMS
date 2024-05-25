from http import HTTPStatus

from companies.factories import AddressFactory
from companies.models import Address
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


class TestCaseAddressModelViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        group_names_with_permission_codenames = {
            "ceos": [
                "add_address",
                "change_address",
                "delete_address",
                "view_address",
            ],
            "accountants": [
                "add_address",
                "change_address",
                "delete_address",
                "view_address",
            ],
            "managers": ["view_address"],
            "hrs": ["view_address"],
        }
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

        cls.password = "testPassword123!"
        cls.user_address = AddressFactory.create()

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.address_list = AddressFactory.create_batch(9)
        self.address = AddressFactory.build()
        self.address_data = {
            "street_name": self.address.street_name,
            "street_number": str(self.address.street_number),
            "city": self.address.city,
            "postcode": self.address.postcode,
            "country": self.address.country,
        }

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password, address=cls.user_address)
        user.groups.add(group)
        return user


class TestCaseUserNotAuthenticatedAddressModelViewSet(TestCaseAddressModelViewSet):
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


class TestCaseUserAccountantAddressModelViewSet(TestCaseAddressModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.accountant = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_list_address_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), 11)

    def test_put_update_address_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), 10)

    def test_delete_address_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), 9)


class TestCaseUserCeoAddressModelViewSet(TestCaseAddressModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_list_address_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), 11)

    def test_put_update_address_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), 10)

    def test_delete_address_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), 9)


class TestCaseUserHrAddressModelViewSet(TestCaseAddressModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.hr = self.create_user_with_group(group_name="hrs")
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_list_address_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_address_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_address_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseUserManagerAddressModelViewSet(TestCaseAddressModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.manager = self.create_user_with_group(group_name="managers")
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_list_address_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_address_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_address_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_address_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_address_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseCreateInstanceAddressModelViewSet(TestCaseAddressModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_not_create_same_address(self):
        self.assertTrue(self.login)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertRaises(serializers.ValidationError)
