from decimal import Decimal
from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django.urls import reverse_lazy
from invoices.factories import InvoiceFactory
from invoices.models import Invoice
from orders.factories import OrderFactory


class OrderDetailViewTests(EDMSTestCase):
    def setUp(self) -> None:
        contract = ContractFactory.create()
        self.order = OrderFactory.create(start_date=contract.start_date)
        self.view_url = reverse_lazy("detail-order", kwargs={"pk": self.order.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "orders/orders/detail_order.html"

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_render_detail_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_detail_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_detail_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_render_detail_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_count_invoices_sum_when_invoices_original_and_correcting_exist(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        seller = CompanyFactory.create()
        buyer = CompanyFactory.create(is_mine=True)
        original = InvoiceFactory.create(seller=seller, buyer=buyer)
        correcting = InvoiceFactory.create(
            seller=seller, buyer=buyer, linked_invoice=original, net_price=Decimal(5999), type=Invoice.CORRECTING
        )
        self.order.cost_invoice.add(original)
        self.order.cost_invoice.add(correcting)
        self.order.save()
        response = self.client.get(self.view_url)
        expected_value = Decimal(5999)
        self.assertEqual(response.context["cost_invoices_net_price_sum"], expected_value)

    def test_count_invoices_sum_when_invoices_duplicate_and_correcting_exist(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        seller = CompanyFactory.create()
        buyer = CompanyFactory.create(is_mine=True)
        duplicate = InvoiceFactory.create(seller=seller, buyer=buyer, type=Invoice.DUPLICATE)
        correcting = InvoiceFactory.create(
            seller=seller, buyer=buyer, linked_invoice=duplicate, net_price=Decimal(5999), type=Invoice.CORRECTING
        )
        self.order.cost_invoice.add(duplicate)
        self.order.cost_invoice.add(correcting)
        self.order.save()
        response = self.client.get(self.view_url)
        expected_value = Decimal(5999)
        self.assertEqual(response.context["cost_invoices_net_price_sum"], expected_value)
