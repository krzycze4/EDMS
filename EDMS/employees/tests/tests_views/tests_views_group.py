from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from users.factories import UserFactory


class GroupUpdateView(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employee = UserFactory.create()
        self.view_url = reverse_lazy("update-group", kwargs={"pk": self.employee.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-employee", kwargs={"pk": self.employee.pk})
        self.template_name = "employees/groups/group_update.html"
        temp_employee_group = get_object_or_404(Group, name="hrs")
        self.employee.groups.add(temp_employee_group)
        self.group_data = {"groups": get_object_or_404(Group, name="managers").pk}

    def test_redirect_to_login_page_when_not_auth_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_redirect_to_login_page_when_not_auth_user_execute_post_method(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_deny_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        response = self.client.post(self.view_url, data=self.group_data)
        self.employee.refresh_from_db()
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        response = self.client.post(self.view_url, data=self.group_data)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.groups.first().pk, self.group_data["groups"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        response = self.client.post(self.view_url, data=self.group_data)
        self.employee.refresh_from_db()
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_deny_update_object_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.assertNotEquals(self.employee.groups.first().pk, self.group_data["groups"])
        response = self.client.post(self.view_url, data=self.group_data)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.groups.first().pk, self.group_data["groups"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)
