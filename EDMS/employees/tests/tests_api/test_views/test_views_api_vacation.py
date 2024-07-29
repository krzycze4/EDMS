from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from employees.factories.factories_vacation import VacationFactory
from employees.models.models_vacation import Vacation
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class VacationApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.vacation_list: List[Vacation] = VacationFactory.create_batch(9)
        leave_user: User = UserFactory.create()
        substitute_users: List[User] = UserFactory.create_batch(2)
        self.vacation: Vacation = VacationFactory.build()
        self.vacation_data = {
            "type": self.vacation.type,
            "start_date": self.vacation.start_date,
            "end_date": self.vacation.end_date,
            "leave_user": leave_user.id,
            "substitute_users": [user.id for user in substitute_users],
            "scan": self.vacation.scan,
            "included_days_off": self.vacation.included_days_off,
        }

    def test_unauthenticated_user_cannot_view_vacation_list(self):
        response = self.client.get(reverse_lazy("vacation-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_vacation_detail(self):
        response = self.client.get(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_vacation(self):
        response = self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_vacation(self):
        response = self.client.put(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_vacation(self):
        response = self.client.delete(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_vacation_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_vacation_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_vacation(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response)

    def test_accountant_cannot_update_vacation(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.vacation_list[0].leave_user, self.vacation_data["leave_user"])

    def test_accountant_cannot_delete_vacation(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.delete(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response)

    def test_ceo_can_view_vacation_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_vacation_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_vacation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response + 1)

    def test_ceo_can_update_vacation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEquals(self.vacation_list[0].leave_user_id, self.vacation_data["leave_user"])

    def test_ceo_can_delete_vacation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.delete(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response - 1)

    def test_hr_can_view_vacation_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_vacation_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_vacation(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response + 1)

    def test_hr_can_update_vacation(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEquals(self.vacation_list[0].leave_user_id, self.vacation_data["leave_user"])

    def test_hr_can_delete_vacation(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.delete(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response - 1)

    def test_manager_can_view_vacation_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_vacation_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_vacation(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response)

    def test_manager_cannot_update_vacation(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.vacation_list[0].leave_user, self.vacation_data["leave_user"])

    def test_manager_cannot_delete_vacation(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_vacation_before_response = Vacation.objects.count()
        response = self.client.delete(
            reverse_lazy("vacation-detail", kwargs={"pk": self.vacation_list[0].id}), self.vacation_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Vacation.objects.count(), count_vacation_before_response)

    def test_prevent_duplicate_vacation_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.client.post(reverse_lazy("vacation-list"), self.vacation_data)
        self.assertRaises(serializers.ValidationError)
