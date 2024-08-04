from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_agreement import Agreement


class AgreementUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.agreement = AgreementFactory.create()
        self.view_url = reverse_lazy("update-agreement", kwargs={"pk": self.agreement.pk})
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/agreements/agreement_update.html"
        self.success_url = reverse_lazy("detail-agreement", kwargs={"pk": self.agreement.pk})
        update_salary_gross = 12000
        self.agreement_data = {
            "name": self.agreement.name,
            "type": self.agreement.type,
            "salary_gross": update_salary_gross,
            "create_date": self.agreement.create_date,
            "start_date": self.agreement.start_date,
            "end_date": self.agreement.end_date,
            "end_date_actual": self.agreement.end_date_actual,
            "user": self.agreement.user.pk,
            "user_display": self.agreement.user,
            "scan": self.agreement.scan,
            "is_current": self.agreement.is_current,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_deny_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_agreement_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.agreement.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn("current_scan", response.context)
        self.assertEqual(response.context["current_scan"], self.agreement.scan)

    def test_update_agreement_and_redirect_to_detail_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.agreement.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertEqual(self.agreement.salary_gross, self.agreement_data["salary_gross"])

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIn("current_scan", response.context)
        self.assertEqual(response.context["current_scan"], self.agreement.scan)

    def test_update_agreement_and_redirect_to_detail_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.agreement.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertEqual(self.agreement.salary_gross, self.agreement_data["salary_gross"])
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
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.agreement.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertNotEquals(self.agreement.salary_gross, self.agreement_data["salary_gross"])
