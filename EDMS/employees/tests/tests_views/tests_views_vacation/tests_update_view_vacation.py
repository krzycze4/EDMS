from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_vacation import VacationFactory
from employees.models.models_vacation import Vacation
from users.factories import UserFactory


class VacationUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        leave_user = UserFactory.create()
        AgreementFactory.create(user=leave_user)
        substitute_users = UserFactory.create_batch(2)
        self.vacation = VacationFactory(leave_user=leave_user, substitute_users=substitute_users)
        self.view_url = reverse_lazy("update-vacation", kwargs={"pk": self.vacation.pk})
        self.login_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.template_name = "employees/vacations/vacation_update.html"
        self.success_url = reverse_lazy("detail-vacation", kwargs={"pk": self.vacation.pk})
        self.vacation_data = {
            "type": Vacation.UNPAID,
            "start_date": self.vacation.start_date,
            "end_date": self.vacation.end_date,
            "included_days_off": self.vacation.included_days_off,
            "leave_user": leave_user.pk,
            "leave_user_display": self.vacation.leave_user,
            "substitute_users": [user.pk for user in substitute_users],
            "scan": self.vacation.scan,
        }

    def test_redirect_to_login_page_when_not_authenticated_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_redirect_to_login_page_when_not_authenticated_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_redirect_url)

    def test_deny_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_object_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])
        response = self.client.post(self.view_url, data=self.vacation_data)
        self.vacation.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        initial_data = response.context["form"].initial
        self.assertEqual(initial_data["leave_user"], self.vacation.leave_user.pk)
        self.assertEqual(initial_data["leave_user_display"], self.vacation.leave_user)

    def test_update_object_and_redirect_to_detail_view_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])
        response = self.client.post(self.view_url, data=self.vacation_data)
        self.vacation.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertEqual(self.vacation.type, self.vacation_data["type"])
        self.assertRedirects(response, self.success_url)

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        initial_data = response.context["form"].initial
        self.assertEqual(initial_data["leave_user"], self.vacation.leave_user.pk)
        self.assertEqual(initial_data["leave_user_display"], self.vacation.leave_user)

    def test_update_object_and_redirect_to_detail_view_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])
        response = self.client.post(self.view_url, data=self.vacation_data)
        self.vacation.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertEqual(self.vacation.type, self.vacation_data["type"])
        self.assertRedirects(response, self.success_url)

    def test_deny_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_agreement_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])
        response = self.client.post(self.view_url, data=self.vacation_data)
        self.vacation.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), expected_value)
        self.assertNotEquals(self.vacation.type, self.vacation_data["type"])