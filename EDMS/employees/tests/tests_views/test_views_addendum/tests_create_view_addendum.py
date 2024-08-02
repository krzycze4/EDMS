from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_addendum import Addendum
from users.factories import UserFactory


class AddendumCreateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.employee = UserFactory.create()
        self.not_logged_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('create-addendum', kwargs={'pk': self.employee.pk})}"
        )
        self.template_name = "employees/addenda/addendum_create.html"
        addendum = AddendumFactory.build()
        agreement = AgreementFactory.create()
        self.addendum_data = {
            "name": addendum.name,
            "agreement": agreement.pk,
            "create_date": addendum.create_date,
            "end_date": addendum.end_date,
            "salary_gross": addendum.salary_gross,
            "scan": addendum.scan,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(
            reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}), data=self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_render_create_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_create_view_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}), data=self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_create_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_create_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}), data=self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        created_addendum_pk = Addendum.objects.last().pk
        self.assertRedirects(response, reverse_lazy("detail-addendum", kwargs={"pk": created_addendum_pk}))

    def test_render_create_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_render_create_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}), data=self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        created_addendum_pk = Addendum.objects.last().pk
        self.assertRedirects(response, reverse_lazy("detail-addendum", kwargs={"pk": created_addendum_pk}))

    def test_render_create_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_create_view_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("create-addendum", kwargs={"pk": self.employee.pk}), data=self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
