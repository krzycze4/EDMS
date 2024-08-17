from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django.urls import reverse_lazy
from invoices.factories import InvoiceFactory
from invoices.models import Invoice


class InvoiceCreateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        buyer = CompanyFactory.create(is_mine=True)
        seller = CompanyFactory.create(is_mine=False)
        self.invoice = InvoiceFactory.build(buyer=buyer, seller=seller)
        self.view_url = reverse_lazy("create-invoice")
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "invoices/create_invoice.html"
        self.invoice_data = {
            "name": self.invoice.name,
            "seller": self.invoice.seller.pk,
            "buyer": self.invoice.buyer.pk,
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

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_render_create_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Invoice.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        success_url = reverse_lazy("detail-invoice", kwargs={"pk": Invoice.objects.last().pk})
        self.assertRedirects(response, success_url)

    def test_render_create_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Invoice.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        success_url = reverse_lazy("detail-invoice", kwargs={"pk": Invoice.objects.last().pk})
        self.assertRedirects(response, success_url)

    def test_deny_render_create_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_object_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Invoice.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), expected_value)

    def test_render_create_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_create_salary_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Invoice.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), expected_value)
