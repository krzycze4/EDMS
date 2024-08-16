from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_termination import TerminationFactory


class TerminationDetailViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        # self.employee = UserFactory.create()
        self.termination = TerminationFactory.create()
        self.view_url = reverse_lazy("detail-termination", kwargs={"pk": self.termination.pk})
        self.redirect_login_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/terminations/termination_detail.html"

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_login_url)

    def test_render_detail_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_detail_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_detail_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_detail_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
