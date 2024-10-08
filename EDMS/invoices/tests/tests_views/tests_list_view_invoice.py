from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils import timezone
from invoices.factories import InvoiceFactory
from invoices.filters import InvoiceFilter
from invoices.models import Invoice

User = get_user_model()


class InvoiceListViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.invoices = InvoiceFactory.create_batch(11)
        self.view_url = reverse_lazy("list-invoice")
        self.view_url_page_2 = f"{reverse_lazy('list-invoice')}?page=2"
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "invoices/list_invoice.html"
        self.invoice = self.invoices[0]
        self.filter_params = {
            "name": self.invoice.name,
            "seller__name": "",
            "buyer__name": "",
            "create_date__gt": "",
            "create_date__lt": "",
        }
        today = timezone.now().date()
        week_ago = today - timezone.timedelta(days=7)
        week_ahead = today + timezone.timedelta(days=7)
        self.invoice_paid = InvoiceFactory(is_paid=True, payment_date=timezone.now().date())
        self.invoice_unpaid_future = InvoiceFactory(is_paid=False, payment_date=week_ahead)
        self.invoice_unpaid_past = InvoiceFactory(is_paid=False, payment_date=week_ago)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_render_list_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_list_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_deny_render_list_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_list_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_pagination(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        objects_per_page = 10
        self.assertEqual(len(response.context["invoices"]), objects_per_page)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")
        response = self.client.get(self.view_url_page_2)
        expected_value = Invoice.objects.count() - objects_per_page
        self.assertEqual(len(response.context["invoices"]), expected_value)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url, data=self.filter_params)
        expected_value = Invoice.objects.filter(name=self.invoice.name).count()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["invoices"]), expected_value)

    def test_filter_unpaid_postponed_invoices_true(self):
        queryset = Invoice.objects.all()
        filter = InvoiceFilter(data={"unpaid": True}, queryset=queryset)
        filtered_qs = filter.qs
        self.assertIn(self.invoice_unpaid_past, filtered_qs)
        self.assertNotIn(self.invoice_paid, filtered_qs)
        self.assertNotIn(self.invoice_unpaid_future, filtered_qs)

    def test_filter_unpaid_postponed_invoices_false(self):
        queryset = Invoice.objects.all()
        filter = InvoiceFilter(data={"unpaid": False}, queryset=queryset)
        filtered_qs = filter.qs
        self.assertIn(self.invoice_paid, filtered_qs)
        self.assertIn(self.invoice_unpaid_future, filtered_qs)
        self.assertIn(self.invoice_unpaid_past, filtered_qs)
