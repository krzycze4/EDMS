from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django import forms
from django.test import RequestFactory
from django.urls import reverse_lazy
from invoices.factories import InvoiceFactory
from invoices.forms import InvoiceForm
from invoices.models import Invoice
from invoices.views import InvoiceUpdateView
from orders.factories import OrderFactory


class InvoiceUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        self.my_company = CompanyFactory.create(is_mine=True)
        self.customer_company = CompanyFactory.create()
        self.invoice = InvoiceFactory.create(seller=self.my_company, buyer=self.customer_company)
        self.view_url = reverse_lazy("update-invoice", kwargs={"pk": self.invoice.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-invoice", kwargs={"pk": self.invoice.pk})
        self.template_name = "invoices/update_invoice.html"
        self.update_invoice_data = {
            "name": self.invoice.name,
            "seller": self.invoice.seller.pk,
            "buyer": self.invoice.buyer.pk,
            "net_price": self.invoice.net_price,
            "vat": 0,
            "gross": self.invoice.net_price,
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
        response = self.client.post(self.view_url, data=self.update_invoice_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_render_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        response = self.client.post(self.view_url, data=self.update_invoice_data)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.vat, self.update_invoice_data["vat"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_render_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        response = self.client.post(self.view_url, data=self.update_invoice_data)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.vat, self.update_invoice_data["vat"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_object_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        response = self.client.post(self.view_url, data=self.update_invoice_data)
        self.invoice.refresh_from_db()
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), expected_value)

    def test_deny_render_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Invoice.objects.count(), expected_value)
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        response = self.client.post(self.view_url, data=self.update_invoice_data)
        self.invoice.refresh_from_db()
        self.assertNotEquals(self.invoice.vat, self.update_invoice_data["vat"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), expected_value)

    def test_get_order_method_when_seller_is_my_company(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        view = InvoiceUpdateView()
        view.object = self.invoice
        order = OrderFactory.create(company=self.customer_company)
        order.income_invoice.add(self.invoice)
        self.assertEqual(view.get_order(), order)

    def test_get_order_method_when_seller_is_not_my_company(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        view = InvoiceUpdateView()
        view.object = self.invoice
        self.invoice.buyer, self.invoice.seller = self.invoice.seller, self.invoice.buyer
        self.invoice.save()
        order = OrderFactory.create(company=self.customer_company)
        order.cost_invoice.add(self.invoice)
        self.assertEqual(view.get_order(), order)

    def test_get_form_method_when_order_exists(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        view = InvoiceUpdateView()
        view.object = self.invoice
        request = RequestFactory().get("/")
        view.request = request
        order = OrderFactory.create(company=self.customer_company)
        order.income_invoice.add(self.invoice)
        form = view.get_form(form_class=InvoiceForm)
        self.assertIsInstance(form.fields["seller"].widget, forms.HiddenInput)
        self.assertIsInstance(form.fields["buyer"].widget, forms.HiddenInput)
        self.assertEqual(form.fields["seller"].label, "")
        self.assertEqual(form.fields["buyer"].label, "")

    def test_get_form_method_when_order_not_exist(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        view = InvoiceUpdateView()
        view.object = self.invoice
        request = RequestFactory().get("/")
        view.request = request
        form = view.get_form(form_class=InvoiceForm)
        self.assertNotIsInstance(form.fields["seller"].widget, forms.HiddenInput)
        self.assertNotIsInstance(form.fields["buyer"].widget, forms.HiddenInput)
        self.assertNotEqual(form.fields["seller"].label, "")
        self.assertNotEqual(form.fields["buyer"].label, "")
