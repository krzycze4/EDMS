from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_agreement import Agreement
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

User = get_user_model()


class AgreementApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.agreement_list: List[Agreement] = AgreementFactory.create_batch(9)
        employee = UserFactory.create()
        self.agreement: Agreement = AgreementFactory.build(user=employee)
        self.agreement_data = {
            "name": self.agreement.name,
            "type": self.agreement.type,
            "salary_gross": self.agreement.salary_gross,
            "create_date": self.agreement.create_date,
            "start_date": self.agreement.start_date,
            "end_date": self.agreement.end_date,
            "end_date_actual": self.agreement.end_date_actual,
            "user": employee.id,
            "scan": self.agreement.scan,
            "is_current": self.agreement.is_current,
        }

    def test_unauthenticated_user_cannot_view_agreement_list(self):
        response = self.client.get(reverse_lazy("agreement-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_agreement_detail(self):
        response = self.client.get(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_agreement(self):
        response = self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_agreement(self):
        response = self.client.put(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_agreement(self):
        response = self.client.delete(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_agreement_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_agreement_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_agreement(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_accountant_cannot_update_agreement(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.put(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_accountant_cannot_delete_agreement(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.delete(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_ceo_can_view_agreement_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_agreement_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_agreement(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response + 1)

    def test_ceo_can_update_agreement(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.put(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_ceo_can_delete_agreement(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.delete(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response - 1)

    def test_hr_can_view_agreement_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_agreement_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_agreement(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response + 1)

    def test_hr_can_update_agreement(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.put(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_hr_can_delete_agreement(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.delete(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response - 1)

    def test_manager_can_view_agreement_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_agreement_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_agreement(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_manager_cannot_update_agreement(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.put(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_manager_cannot_delete_agreement(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_agreement_before_response = Agreement.objects.count()
        response = self.client.delete(
            reverse_lazy("agreement-detail", kwargs={"pk": self.agreement_list[0].id}), self.agreement_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Agreement.objects.count(), count_agreement_before_response)

    def test_prevent_duplicate_agreement_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.client.post(reverse_lazy("agreement-list"), self.agreement_data)
        self.assertRaises(serializers.ValidationError)
