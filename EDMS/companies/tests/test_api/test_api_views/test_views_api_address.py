from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import AddressFactory
from companies.models import Address
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient

User = get_user_model()


class AddressApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.address_list: List[Address] = AddressFactory.create_batch(9)
        self.address: Address = AddressFactory.build()
        self.address_data = {
            "street_name": self.address.street_name,
            "street_number": str(self.address.street_number),
            "city": self.address.city,
            "postcode": self.address.postcode,
            "country": self.address.country,
        }

    def test_unauthenticated_user_cannot_view_address_list(self):
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_address_detail(self):
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_address(self):
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_address(self):
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_address(self):
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_address_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_address_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_create_address(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), count_address_before_response + 1)

    def test_accountant_can_update_address(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), count_address_before_response)

    def test_accountant_can_delete_address(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), count_address_before_response - 1)

    def test_ceo_can_view_address_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_address_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_address(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), count_address_before_response + 1)

    def test_ceo_can_update_address(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), count_address_before_response)

    def test_ceo_can_delete_address(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Address.objects.count(), count_address_before_response - 1)

    def test_hr_can_view_address_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_address_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_address(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Address.objects.count(), count_address_before_response + 1)

    def test_hr_can_update_address(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Address.objects.count()
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Address.objects.count(), count_address_before_response)

    def test_hr_cannot_delete_address(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_can_view_address_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_address_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_address(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_cannot_update_address(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_cannot_delete_address(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.delete(
            reverse_lazy("address-detail", kwargs={"pk": self.address_list[0].id}), self.address_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_prevent_duplicate_address_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.client.post(reverse_lazy("address-list"), self.address_data)
        self.assertRaises(serializers.ValidationError)
