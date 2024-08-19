from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django.urls import reverse_lazy
from invoices.factories import InvoiceFactory
from invoices.models import Invoice
from orders.factories import OrderFactory


class InvoiceDetailViewTests(EDMSTestCase):
    def setUp(self) -> None:
        self.my_company = CompanyFactory(is_mine=True)
        self.customer_company = CompanyFactory()
        self.invoice = InvoiceFactory.create(seller=self.my_company, buyer=self.customer_company)
        self.view_url = reverse_lazy("detail-invoice", kwargs={"pk": self.invoice.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "invoices/detail_invoice.html"

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url)
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

    def test_check_context_data(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertIn("child_invoices", response.context)
        self.assertIn("order_from_income_invoice", response.context)
        self.assertIn("order_from_cost_invoice", response.context)

    def test_get_child_invoices_when_invoice_is_original(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        duplicate = InvoiceFactory.create(
            linked_invoice=self.invoice, seller=self.my_company, buyer=self.customer_company, type=Invoice.DUPLICATE
        )
        proforma = InvoiceFactory.create(
            linked_invoice=self.invoice, seller=self.my_company, buyer=self.customer_company, type=Invoice.PROFORMA
        )
        response = self.client.get(self.view_url)
        self.assertEqual(list(response.context["child_invoices"]), [duplicate, proforma])

    def test_get_child_invoices_when_invoice_is_duplicate(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.invoice.type = Invoice.DUPLICATE
        self.invoice.save()
        proforma = InvoiceFactory.create(
            linked_invoice=self.invoice, seller=self.my_company, buyer=self.customer_company, type=Invoice.PROFORMA
        )
        response = self.client.get(self.view_url)
        self.assertEqual(list(response.context["child_invoices"]), [proforma])

    def test_get_child_invoices_when_no_child_invoices(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(list(response.context["child_invoices"]), [])

    def test_get_child_invoices_when_invoice_is_not_original_or_duplicate(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.invoice.type = Invoice.PROFORMA
        self.invoice.save()
        response = self.client.get(self.view_url)
        self.assertEqual(response.context["child_invoices"], None)

    def test_order_from_income_invoice(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contract = ContractFactory.create(company=self.customer_company)
        order = OrderFactory.create(contract=contract)
        order.income_invoice.add(self.invoice)
        response = self.client.get(self.view_url)
        self.assertEqual(list(response.context["order_from_income_invoice"]), [order])
        self.assertEqual(list(response.context["order_from_cost_invoice"]), [])

    def test_order_from_cost_invoice(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contract = ContractFactory.create(company=self.customer_company)
        order = OrderFactory.create(contract=contract)
        order.cost_invoice.add(self.invoice)
        response = self.client.get(self.view_url)
        self.assertEqual(list(response.context["order_from_income_invoice"]), [])
        self.assertEqual(list(response.context["order_from_cost_invoice"]), [order])
