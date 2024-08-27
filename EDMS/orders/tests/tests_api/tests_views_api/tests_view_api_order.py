from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from orders.factories import OrderFactory
from orders.models import Order
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class OrderApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.order_list: List[Order] = OrderFactory.create_batch(9)
        company = CompanyFactory.create()
        contract = ContractFactory.create(company=company)
        user = UserFactory.create()
        self.order = OrderFactory.build(company=company, contract=contract, user=user)
        self.order_create_data = {
            "name": self.order.name,
            "payment": self.order.payment,
            "company": company.pk,
            "create_date": self.order.create_date.strftime("%Y-%m-%d"),
            "start_date": self.order.start_date.strftime("%Y-%m-%d"),
            "end_date": self.order.end_date.strftime("%Y-%m-%d"),
            "contract": contract.pk,
            "description": self.order.description,
        }
        self.order_update_data = {
            "name": self.order.name,
            "company": company.pk,
            "payment": 123123,
            "status": Order.CLOSED,
            "create_date": self.order.create_date.strftime("%Y-%m-%d"),
            "start_date": self.order.start_date.strftime("%Y-%m-%d"),
            "end_date": self.order.start_date.strftime("%Y-%m-%d"),
            "description": self.order.description,
        }
        self.list_url = reverse_lazy("order-list")
        self.detail_url = reverse_lazy("order-detail", kwargs={"pk": self.order_list[0].id})

    def test_unauthenticated_user_cannot_view_object_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_object_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_object(self):
        response = self.client.post(self.list_url, self.order_create_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_object(self):
        response = self.client.put(self.detail_url, self.order_update_data)
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

    def test_accountant_can_create_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.post(self.list_url, self.order_create_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), count_object_before_response)

    def test_accountant_cannot_update_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = Order.objects.count()
        expected_value = Order.CLOSED
        self.assertNotEquals(self.order.status, expected_value)
        response = self.client.put(self.detail_url, self.order_update_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.order.status, expected_value)
        self.assertEqual(Order.objects.count(), count_invoice_before_response)

    def test_accountant_cannot_delete_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), count_object_before_response)

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

    def test_ceo_can_create_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.post(self.list_url, self.order_create_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Order.objects.count(), count_object_before_response + 1)

    def test_ceo_can_update_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.order.save()
        count_object_before_response = Order.objects.count()
        expected_value = Order.CLOSED
        self.assertNotEquals(self.order.status, expected_value)
        response = self.client.put(self.detail_url, self.order_update_data)
        self.order.refresh_from_db()
        expected_value = Order.OPEN
        self.assertEqual(self.order.status, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Order.objects.count(), count_object_before_response)

    def test_ceo_can_delete_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Order.objects.count(), count_object_before_response - 1)

    def test_hr_cannot_view_object_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_hr_cannot_view_object_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_hr_cannot_create_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.post(self.list_url, self.order_create_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), count_object_before_response)

    def test_hr_cannot_update_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        expected_value = Order.CLOSED
        self.assertNotEquals(self.order.status, expected_value)
        response = self.client.put(self.detail_url, self.order_update_data)
        self.assertNotEquals(self.order.status, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), count_object_before_response)

    def test_hr_cannot_delete_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = Order.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), count_invoice_before_response)

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

    def test_manager_can_create_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.post(self.list_url, self.order_create_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Order.objects.count(), count_object_before_response + 1)

    def test_manager_can_update_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.order.save()
        count_object_before_response = Order.objects.count()
        expected_value = Order.CLOSED
        self.assertNotEquals(self.order.status, expected_value)
        response = self.client.put(self.detail_url, self.order_update_data)
        self.order.refresh_from_db()
        expected_value = Order.OPEN
        self.assertEqual(self.order.status, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Order.objects.count(), count_object_before_response)

    def test_manager_can_delete_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Order.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Order.objects.count(), count_object_before_response - 1)

    def test_prevent_duplicate_object_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(self.list_url, self.order_create_data)
        self.client.post(self.list_url, self.order_create_data)
        self.assertRaises(serializers.ValidationError)
