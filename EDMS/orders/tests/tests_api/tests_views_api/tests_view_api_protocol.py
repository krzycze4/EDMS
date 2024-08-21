from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Protocol
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class ProtocolApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        order = OrderFactory.create()
        self.protocol_list: List[Protocol] = ProtocolFactory.create_batch(9)
        user = UserFactory.create()
        self.protocol = ProtocolFactory.create()
        self.protocol_data = {
            "name": self.protocol.name,
            "scan": self.protocol.scan,
            "create_date": self.protocol.create_date,
            "user": user.pk,
            "order": order.pk,
        }
        self.list_url = reverse_lazy("protocol-list")
        self.detail_url = reverse_lazy("protocol-detail", kwargs={"pk": self.protocol.id})

    def test_unauthenticated_user_cannot_view_object_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_object_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_object(self):
        response = self.client.post(self.list_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_object(self):
        response = self.client.put(self.detail_url, self.protocol_data)
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
        count_object_before_response = Protocol.objects.count()
        response = self.client.post(self.list_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_accountant_cannot_update_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.put(self.detail_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_accountant_cannot_delete_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

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
        count_object_before_response = Protocol.objects.count()
        response = self.client.post(self.list_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Protocol.objects.count(), count_object_before_response + 1)

    def test_ceo_can_update_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.put(self.detail_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_ceo_can_delete_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Protocol.objects.count(), count_object_before_response - 1)

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
        count_object_before_response = Protocol.objects.count()
        response = self.client.post(self.list_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_hr_cannot_update_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.put(self.detail_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_hr_cannot_delete_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = Protocol.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), count_invoice_before_response)

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
        self.protocol.delete()
        count_object_before_response = Protocol.objects.count()
        response = self.client.post(self.list_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Protocol.objects.count(), count_object_before_response + 1)

    def test_manager_can_update_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.put(self.detail_url, self.protocol_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Protocol.objects.count(), count_object_before_response)

    def test_manager_can_delete_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Protocol.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Protocol.objects.count(), count_object_before_response - 1)
