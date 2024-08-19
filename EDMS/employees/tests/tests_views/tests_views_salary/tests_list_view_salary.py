from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from employees.factories.factories_salary import SalaryFactory
from employees.models.models_salaries import Salary

User = get_user_model()


class SalaryListViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.salaries = SalaryFactory.create_batch(11)
        self.view_url = reverse_lazy("list-salary")
        self.view_url_page_2 = f"{reverse_lazy('list-salary')}?page=2"
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/salaries/salary_list.html"
        self.salary = self.salaries[0]
        self.filter_params = {
            "user_first_name": self.salary.user.first_name,
            "user_last_name": self.salary.user.last_name,
            "date__gte": "",
            "date__lte": "",
            "fee__gte": "",
            "fee__lte": "",
        }

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

    def test_render_list_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_deny_render_list_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_pagination(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        objects_per_page = 10
        self.assertEqual(len(response.context["salaries"]), objects_per_page)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")
        response = self.client.get(self.view_url_page_2)
        expected_value = Salary.objects.count() - objects_per_page
        self.assertEqual(len(response.context["salaries"]), expected_value)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)

        response = self.client.get(self.view_url, data=self.filter_params)

        expected_value = Salary.objects.filter(
            user__first_name__icontains=self.salary.user.first_name,
            user__last_name__icontains=self.salary.user.last_name,
        ).count()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context["salaries"]), expected_value)
