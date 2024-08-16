from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_salary import SalaryFactory
from employees.models.models_salaries import Salary
from users.factories import UserFactory


class SalaryCreateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        salary = SalaryFactory.create()
        self.view_url = reverse_lazy("create-salary")
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-salary", kwargs={"pk": salary.pk + 1})
        self.template_name = "employees/salaries/salary_create.html"
        employee = UserFactory.create()
        new_salary = SalaryFactory.build()
        self.new_salary_data = {
            "date": new_salary.date,
            "user": employee.pk,
            "fee": new_salary.fee,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.new_salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_render_create_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_salary_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Salary.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.new_salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Salary.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_render_create_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_salary_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Salary.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.new_salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Salary.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_render_create_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_salary_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Salary.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.new_salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_value += 1
        self.assertEqual(Salary.objects.count(), expected_value)
        self.assertRedirects(response, self.success_url)

    def test_render_create_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_create_salary_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Salary.objects.count(), expected_value)
        response = self.client.post(self.view_url, data=self.new_salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Salary.objects.count(), expected_value)
