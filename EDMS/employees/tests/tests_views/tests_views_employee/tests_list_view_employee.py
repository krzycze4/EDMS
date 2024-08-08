from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from users.factories import UserFactory

User = get_user_model()


class EmployeeListView(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employees = UserFactory.create_batch(11)
        self.view_url = reverse_lazy("list-employee")
        self.view_url_page_2 = f"{reverse_lazy('list-employee')}?page=2"
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/employees/employee_list.html"
        self.employee = self.employees[0]
        self.filter_params = {
            "first_name__icontains": self.employee.first_name,
            "last_name__icontains": self.employee.last_name,
            "email__icontains": "",
            "phone_number__exact": "",
            "position__exact": "",
            "is_active__exact": "",
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

    def test_render_list_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_pagination(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        objects_per_page = 10
        self.assertEqual(len(response.context["users"]), objects_per_page)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")
        response = self.client.get(self.view_url_page_2)
        expected_value = User.objects.count() - objects_per_page
        self.assertEqual(len(response.context["users"]), expected_value)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_filter(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url, data=self.filter_params)
        expected_value = User.objects.filter(
            first_name__exact=self.employee.first_name, last_name__exact=self.employee.last_name
        ).count()
        self.assertEqual(len(response.context["users"]), expected_value)
