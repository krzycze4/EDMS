from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_termination import Termination
from users.factories import UserFactory


class TerminationCreateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employee = UserFactory.create()
        agreement = AgreementFactory.create()
        self.termination = TerminationFactory.build()
        self.view_url = reverse_lazy("create-termination", kwargs={"pk": self.employee.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/terminations/termination_create.html"
        self.termination_data = {
            "name": self.termination.name,
            "agreement": agreement.pk,
            "create_date": self.termination.create_date,
            "end_date": self.termination.end_date,
            "scan": self.termination.scan,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_deny_render_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Termination.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), expected_value)

    def test_render_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_and_redirect_to_detail_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Termination.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Termination.objects.count(), expected_value)
        success_url = reverse_lazy("detail-termination", kwargs={"pk": Termination.objects.last().pk})
        self.assertRedirects(response, success_url)

    def test_render_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_object_and_redirect_to_detail_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Termination.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Termination.objects.count(), expected_value)
        success_url = reverse_lazy("detail-termination", kwargs={"pk": Termination.objects.last().pk})
        self.assertRedirects(response, success_url)

    def test_deny_render_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Termination.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), expected_value)
