from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy

User = get_user_model()


class PasswordUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        self.view_url = reverse_lazy("change-password")
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/passwords/change_password.html"
        # self.success_url = reverse_lazy("detail-employee", kwargs={"pk": ...})
        self.new_password = User.objects.make_random_password()
        self.correct_password_data = {
            "old_password": self.password,
            "new_password1": self.new_password,
            "new_password2": self.new_password,
        }
        self.incorrect_password_data = {
            "old_password": self.password,
            "new_password1": self.new_password,
            "new_password2": User.objects.make_random_password(),
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.accountant.password))
        response = self.client.post(self.view_url, data=self.correct_password_data)
        self.accountant.refresh_from_db()
        self.assertTrue(check_password(self.new_password, self.accountant.password))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        success_url = reverse_lazy("detail-employee", kwargs={"pk": self.accountant.pk})
        self.assertRedirects(response, success_url)

    def test_deny_update_object_when_form_invalid_different_new_passwords_logged_user_group_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.accountant.password))
        response = self.client.post(self.view_url, data=self.incorrect_password_data)
        self.accountant.refresh_from_db()
        self.assertFalse(check_password(self.new_password, self.accountant.password))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.ceo.password))
        response = self.client.post(self.view_url, data=self.correct_password_data)
        self.ceo.refresh_from_db()
        self.assertTrue(check_password(self.new_password, self.ceo.password))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        success_url = reverse_lazy("detail-employee", kwargs={"pk": self.ceo.pk})
        self.assertRedirects(response, success_url)

    def test_deny_update_object_when_form_invalid_different_new_passwords_and_logged_user_group_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.accountant.password))
        response = self.client.post(self.view_url, data=self.incorrect_password_data)
        self.ceo.refresh_from_db()
        self.assertFalse(check_password(self.new_password, self.accountant.password))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.manager.password))
        response = self.client.post(self.view_url, data=self.correct_password_data)
        self.manager.refresh_from_db()
        self.assertTrue(check_password(self.new_password, self.manager.password))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        success_url = reverse_lazy("detail-employee", kwargs={"pk": self.manager.pk})
        self.assertRedirects(response, success_url)

    def test_deny_update_object_when_form_invalid_different_new_passwords_and_logged_user_group_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.manager.password))
        response = self.client.post(self.view_url, data=self.incorrect_password_data)
        self.manager.refresh_from_db()
        self.assertFalse(check_password(self.new_password, self.manager.password))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_object_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.hr.password))
        response = self.client.post(self.view_url, data=self.correct_password_data)
        self.hr.refresh_from_db()
        self.assertTrue(check_password(self.new_password, self.hr.password))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        success_url = reverse_lazy("detail-employee", kwargs={"pk": self.hr.pk})
        self.assertRedirects(response, success_url)

    def test_deny_update_object_when_form_invalid_different_new_passwords_and_logged_user_group_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue(check_password(self.password, self.hr.password))
        response = self.client.post(self.view_url, data=self.incorrect_password_data)
        self.hr.refresh_from_db()
        self.assertFalse(check_password(self.new_password, self.hr.password))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
