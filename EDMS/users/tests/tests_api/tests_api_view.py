from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import AddressFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class UserApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.user_list: List[User] = UserFactory.create_batch(9)
        address = AddressFactory.create()
        self.user = UserFactory.build()
        password = User.objects.make_random_password()
        self.user_data = {
            "first_name": "firstname",
            "last_name": self.user.last_name,
            "email": self.user.email,
            "password": password,
            "is_active": self.user.is_active,
            "phone_number": self.user.phone_number,
            "position": self.user.position,
            "vacation_days_per_year": self.user.vacation_days_per_year,
            "address": address.pk,
        }
        self.list_url = reverse_lazy("user-list")
        self.detail_url = reverse_lazy("user-detail", kwargs={"pk": self.user_list[0].id})

    def test_unauthenticated_user_cannot_view_object_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_object_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_object(self):
        response = self.client.post(self.list_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_object(self):
        response = self.client.put(self.detail_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_object(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_object_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_object_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.post(self.list_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_accountant_cannot_update_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        expected_value = self.user_data["first_name"]
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        response = self.client.put(self.detail_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_accountant_cannot_delete_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_ceo_can_view_object_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_object_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_cannot_create_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.post(self.list_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_ceo_can_update_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        expected_value = self.user_data["first_name"]
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        response = self.client.put(self.detail_url, self.user_data)
        self.user_list[0].refresh_from_db()
        self.assertEqual(self.user_list[0].first_name, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_ceo_cannot_delete_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_hr_can_view_object_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_object_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_cannot_create_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.post(self.list_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_hr_can_update_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        expected_value = self.user_data["first_name"]
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        response = self.client.put(self.detail_url, self.user_data)
        self.user_list[0].refresh_from_db()
        self.assertEqual(self.user_list[0].first_name, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_hr_cannot_delete_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = User.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_invoice_before_response)

    def test_manager_can_view_object_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_object_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.post(self.list_url, self.user_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_manager_cannot_update_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        expected_value = self.user_data["first_name"]
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        response = self.client.put(self.detail_url, self.user_data)
        self.user_list[0].refresh_from_db()
        self.assertNotEquals(self.user_list[0].first_name, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)

    def test_manager_cannot_delete_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = User.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(User.objects.count(), count_object_before_response)
