from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from contracts.factories import ContractFactory
from django.urls import reverse_lazy
from orders.factories import OrderFactory
from orders.models import Order
from users.factories import UserFactory


class InvoiceUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        contract = ContractFactory.create()
        self.order = OrderFactory.create(
            company=contract.company, user=self.user, contract=contract, start_date=contract.start_date
        )
        self.view_url = reverse_lazy("update-order", kwargs={"pk": self.order.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-order", kwargs={"pk": self.order.pk})
        self.template_name = "orders/orders/update_order.html"
        self.order_data = {
            "company": self.order.company.pk,
            "payment": 123123,
            "status": self.order.status,
            "start_date": self.order.start_date,
            "create_date": self.order.create_date,
            "end_date": self.order.end_date,
            "description": self.order.description,
            "contract": self.order.contract.pk,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.order_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_deny_render_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Order.objects.count(), expected_value)
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        response = self.client.post(self.view_url, data=self.order_data)
        self.order.refresh_from_db()
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), expected_value)

    def test_render_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Order.objects.count(), expected_value)
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        response = self.client.post(self.view_url, data=self.order_data)
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment, self.order_data["payment"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Order.objects.count(), expected_value)
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
        self.assertEqual(Order.objects.count(), expected_value)
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        response = self.client.post(self.view_url, data=self.order_data)
        self.order.refresh_from_db()
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Order.objects.count(), expected_value)

    def test_render_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_deny_create_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Order.objects.count(), expected_value)
        self.assertNotEquals(self.order.payment, self.order_data["payment"])
        response = self.client.post(self.view_url, data=self.order_data)
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment, self.order_data["payment"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Order.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)
