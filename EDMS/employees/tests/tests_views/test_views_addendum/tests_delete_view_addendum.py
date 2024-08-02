from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_addendum import AddendumFactory
from employees.models.models_addendum import Addendum


class AddendumDeleteViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.addendum = AddendumFactory.create()
        self.not_logged_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('delete-addendum', kwargs={'pk': self.addendum.pk})}"
        )
        self.success_url = reverse_lazy("detail-employee", kwargs={"pk": self.addendum.agreement.user.pk})
        self.view_url = reverse_lazy("delete-addendum", kwargs={"pk": self.addendum.pk})
        self.template_name = "employees/addenda/addendum_delete.html"

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_deny_render_delete_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_delete_addendum_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Addendum.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        self.assertEqual(Addendum.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_delete_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete_addendum_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Addendum.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        expected_value = 0
        self.assertEqual(Addendum.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_deny_render_delete_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_delete_addendum_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Addendum.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        self.assertEqual(Addendum.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_delete_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete_addendum_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Addendum.objects.count(), expected_value)
        response = self.client.post(self.view_url)
        expected_value = 0
        self.assertEqual(Addendum.objects.count(), expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)
