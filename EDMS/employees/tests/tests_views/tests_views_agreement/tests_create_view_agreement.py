from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_agreement import Agreement
from users.factories import UserFactory


class AgreementCreateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employee = UserFactory.create()
        self.view_url = reverse_lazy("create-agreement", kwargs={"pk": self.employee.pk})
        self.not_logged_user_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-employee", kwargs={"pk": self.employee.pk})
        self.template_name = "employees/agreements/agreement_create.html"
        agreement = AgreementFactory.build()
        self.agreement_data = {
            "name": agreement.name,
            "type": agreement.type,
            "salary_gross": agreement.salary_gross,
            "create_date": agreement.create_date,
            "start_date": agreement.start_date,
            "end_date": agreement.end_date,
            "end_date_actual": agreement.end_date_actual,
            "user": self.employee.pk,
            "user_display": self.employee,
            "scan": agreement.scan,
            "is_current": agreement.is_current,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_deny_render_create_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_agreement_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Agreement.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), expected_value)

    def test_render_create_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_agreement_and_redirect_to_detail_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Agreement.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value = 1
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_render_create_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_agreement_and_redirect_to_detail_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Agreement.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.agreement_data)
        expected_value = 1
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_create_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_create_agreement_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 0
        self.assertEqual(Agreement.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.agreement_data)
        self.assertEqual(Agreement.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
