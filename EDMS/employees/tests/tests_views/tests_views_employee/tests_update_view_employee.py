from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from users.factories import UserFactory

User = get_user_model()


class EmployeeDetailViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employee = UserFactory.create()
        self.view_url = reverse_lazy("update-employee-contact", kwargs={"pk": self.employee.pk})
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/employees/employee_update.html"
        self.success_url = reverse_lazy("detail-employee", kwargs={"pk": self.employee.pk})
        update_employee = UserFactory.build()
        self.employee_data = {
            "first_name": self.employee.first_name,
            "last_name": self.employee.last_name,
            "email": self.employee.email,
            "phone_number": update_employee.phone_number,
            "position": self.employee.position,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.employee_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_deny_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_employee_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        response = self.client.post(self.view_url, data=self.employee_data)
        self.employee.refresh_from_db()
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_employee_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 5
        self.assertEqual(User.objects.count(), expected_value)
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        response = self.client.post(self.view_url, data=self.employee_data)
        self.employee.refresh_from_db()
        self.assertEqual(User.objects.count(), expected_value)
        self.assertEqual(self.employee.phone_number, self.employee_data["phone_number"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_employee_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        response = self.client.post(self.view_url, data=self.employee_data)
        self.employee.refresh_from_db()
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_employee_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 5
        self.assertEqual(User.objects.count(), expected_value)
        self.assertNotEquals(self.employee.phone_number, self.employee_data["phone_number"])
        response = self.client.post(self.view_url, data=self.employee_data)
        self.employee.refresh_from_db()
        self.assertEqual(User.objects.count(), expected_value)
        self.assertEqual(self.employee.phone_number, self.employee_data["phone_number"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)
