from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_agreement import Agreement
from employees.models.models_termination import Termination


class TerminationUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        agreement = AgreementFactory.create()
        self.termination = TerminationFactory.create(agreement=agreement)
        self.view_url = reverse_lazy("update-termination", kwargs={"pk": self.termination.pk})
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/terminations/termination_update.html"
        self.success_url = reverse_lazy("detail-termination", kwargs={"pk": self.termination.pk})
        updated_termination_name = "Termination 99"
        self.termination_data = {
            "name": updated_termination_name,
            "create_date": self.termination.create_date,
            "agreement": agreement,
            "end_date": self.termination.end_date,
            "scan": self.termination.scan,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_deny_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])
        response = self.client.post(self.view_url, data=self.termination_data)
        self.termination.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_and_redirect_to_detail_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])
        response = self.client.post(self.view_url, data=self.termination_data)
        self.termination.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertEqual(self.termination.name, self.termination_data["name"])
        self.assertRedirects(response, self.success_url)

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_and_redirect_to_detail_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])
        response = self.client.post(self.view_url, data=self.termination_data)
        self.termination.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertEqual(self.termination.name, self.termination_data["name"])
        self.assertRedirects(response, self.success_url)

    def test_deny_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_agreement_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])
        response = self.client.post(self.view_url, data=self.termination_data)
        self.termination.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), expected_value)
        self.assertNotEquals(self.termination.name, self.termination_data["name"])
