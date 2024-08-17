from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from invoices.factories import InvoiceFactory
from invoices.models import Invoice
from rest_framework import serializers
from rest_framework.test import APIClient

User = get_user_model()


class InvoiceApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.invoice_list: List[Invoice] = InvoiceFactory.create_batch(9)
        self.invoice = InvoiceFactory.build()
        buyer = CompanyFactory.create()
        seller = CompanyFactory.create()
        self.invoice_data = {
            "name": self.invoice.name,
            "seller": seller.pk,
            "buyer": buyer.pk,
            "net_price": self.invoice.net_price,
            "vat": self.invoice.vat,
            "gross": self.invoice.gross,
            "create_date": self.invoice.create_date,
            "service_date": self.invoice.service_date,
            "payment_date": self.invoice.payment_date,
            "type": self.invoice.type,
            "linked_invoice": "",
            "scan": self.invoice.scan,
            "is_paid": self.invoice.is_paid,
        }
        self.list_url = reverse_lazy("invoice-list")
        self.detail_url = reverse_lazy("invoice-detail", kwargs={"pk": self.invoice_list[0].id})

    def test_unauthenticated_user_cannot_view_object_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_object_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_object(self):
        response = self.client.post(self.list_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_object(self):
        response = self.client.put(self.detail_url, self.invoice_data)
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
        count_object_before_response = Invoice.objects.count()
        response = self.client.post(self.list_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Invoice.objects.count(), count_object_before_response + 1)

    def test_accountant_can_update_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = Invoice.objects.count()
        response = self.client.put(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Invoice.objects.count(), count_invoice_before_response)

    def test_accountant_can_delete_object(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), count_object_before_response - 1)

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
        count_object_before_response = Invoice.objects.count()
        response = self.client.post(self.list_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Invoice.objects.count(), count_object_before_response + 1)

    def test_ceo_can_update_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.put(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_ceo_can_delete_object(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.delete(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), count_object_before_response - 1)

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
        count_object_before_response = Invoice.objects.count()
        response = self.client.post(self.list_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_hr_cannot_update_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.put(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_hr_cannot_delete_object(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_invoice_before_response = Invoice.objects.count()
        response = self.client.delete(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_invoice_before_response)

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
        count_object_before_response = Invoice.objects.count()
        response = self.client.post(self.list_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_manager_cannot_update_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.put(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_manager_cannot_delete_object(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_object_before_response = Invoice.objects.count()
        response = self.client.delete(self.detail_url, self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), count_object_before_response)

    def test_prevent_duplicate_addendum_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(self.list_url, self.invoice_data)
        self.client.post(self.list_url, self.invoice_data)
        self.assertRaises(serializers.ValidationError)
