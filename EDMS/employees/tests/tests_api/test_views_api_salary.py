from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from employees.factories.factories_salary import SalaryFactory
from employees.models.models_salaries import Salary
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class SalaryApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.salary_list: List[Salary] = SalaryFactory.create_batch(9)
        employee = UserFactory.create()
        self.salary: Salary = SalaryFactory.build(user=employee)
        self.salary_data = {
            "date": self.salary.date,
            "user": employee.id,
            "fee": self.salary.fee,
        }

    def test_unauthenticated_user_cannot_view_salary_list(self):
        response = self.client.get(reverse_lazy("salary-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_salary_detail(self):
        response = self.client.get(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_salary(self):
        response = self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_salary(self):
        response = self.client.put(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_salary(self):
        response = self.client.delete(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_salary_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_salary_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_create_salary(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Salary.objects.count(), count_salary_before_response + 1)

    def test_accountant_can_update_salary(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.put(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_accountant_can_delete_salary(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.delete(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Salary.objects.count(), count_salary_before_response - 1)

    def test_ceo_can_view_salary_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_salary_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_salary(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Salary.objects.count(), count_salary_before_response + 1)

    def test_ceo_can_update_salary(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.put(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_ceo_can_delete_salary(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.delete(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Salary.objects.count(), count_salary_before_response - 1)

    def test_hr_can_view_salary_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_salary_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_salary(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Salary.objects.count(), count_salary_before_response + 1)

    def test_hr_can_update_salary(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.put(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_hr_can_delete_salary(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.delete(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Salary.objects.count(), count_salary_before_response - 1)

    def test_manager_cannot_view_salary_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_cannot_view_salary_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_manager_cannot_create_salary(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_manager_cannot_update_salary(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.put(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_manager_cannot_delete_salary(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_salary_before_response = Salary.objects.count()
        response = self.client.delete(
            reverse_lazy("salary-detail", kwargs={"pk": self.salary_list[0].id}), self.salary_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Salary.objects.count(), count_salary_before_response)

    def test_prevent_duplicate_salary_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.client.post(reverse_lazy("salary-list"), self.salary_data)
        self.assertRaises(serializers.ValidationError)
