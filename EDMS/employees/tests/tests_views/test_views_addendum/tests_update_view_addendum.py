from decimal import Decimal
from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from employees.factories.factories_addendum import AddendumFactory
from employees.models.models_addendum import Addendum


class AddendumUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.addendum = AddendumFactory.create()
        addendum_update = AddendumFactory.build(salary_gross=Decimal(10000))
        self.addendum_update_data = {
            "name": self.addendum.name,
            "agreement": self.addendum.agreement.pk,
            "create_date": self.addendum.create_date,
            "end_date": self.addendum.end_date,
            "salary_gross": addendum_update.salary_gross,
            "scan": self.addendum.scan,
        }
        self.not_logged_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('update-addendum', kwargs={'pk': self.addendum.pk})}"
        )
        self.template_name = "employees/addenda/addendum_update.html"

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(
            reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}), data=self.addendum_update_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_addendum_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = self.addendum.salary_gross
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        response = self.client.post(
            reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}), data=self.addendum_update_data
        )
        expected_value = self.addendum.salary_gross
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_addendum_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = self.addendum.salary_gross
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        response = self.client.post(
            reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}), data=self.addendum_update_data
        )
        expected_value = self.addendum_update_data["salary_gross"]
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("detail-addendum", kwargs={"pk": self.addendum.pk}))

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_addendum_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = self.addendum.salary_gross
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        response = self.client.post(
            reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}), data=self.addendum_update_data
        )
        expected_value = self.addendum_update_data["salary_gross"]
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("detail-addendum", kwargs={"pk": self.addendum.pk}))

    def test_deny_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_view_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = self.addendum.salary_gross
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        response = self.client.post(
            reverse_lazy("update-addendum", kwargs={"pk": self.addendum.pk}), data=self.addendum_update_data
        )
        self.assertEqual(get_object_or_404(Addendum, pk=self.addendum.pk).salary_gross, expected_value)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
