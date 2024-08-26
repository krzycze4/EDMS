from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from contracts.factories import ContractFactory
from django.urls import reverse_lazy
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Protocol
from users.factories import UserFactory


class ProtocolDeleteViewTests(EDMSTestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        contract = ContractFactory.create()
        self.order = OrderFactory.create(
            company=contract.company, user=self.user, contract=contract, start_date=contract.start_date
        )
        self.protocol = ProtocolFactory.create(user=self.user, order=self.order)
        self.view_url = reverse_lazy("delete-protocol", kwargs={"pk": self.protocol.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "orders/protocols/delete_protocol.html"
        self.success_url = reverse_lazy("detail-order", kwargs={"pk": self.order.pk})

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_deny_render_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_delete_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Protocol.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), expected_value)

    def test_render_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Protocol.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value -= 1
        self.assertEqual(Protocol.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_delete_object_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Protocol.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Protocol.objects.count(), expected_value)

    def test_render_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Protocol.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        expected_value -= 1
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Protocol.objects.count(), expected_value)
