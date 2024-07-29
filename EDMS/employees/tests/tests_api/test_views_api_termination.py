from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.urls import reverse_lazy
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_termination import Termination
from rest_framework import serializers
from rest_framework.test import APIClient


class TerminationApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.termination_list: List[Termination] = TerminationFactory.create_batch(9)
        agreement = AgreementFactory.create()
        self.termination: Termination = TerminationFactory.build(agreement=agreement)
        self.termination_data = {
            "name": self.termination.name,
            "agreement": agreement.id,
            "create_date": self.termination.create_date,
            "end_date": self.termination.end_date,
            "scan": self.termination.scan,
        }

    def test_unauthenticated_user_cannot_view_termination_list(self):
        response = self.client.get(reverse_lazy("termination-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_termination_detail(self):
        response = self.client.get(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_termination(self):
        response = self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_termination(self):
        response = self.client.put(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_termination(self):
        response = self.client.delete(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_termination_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_termination_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_termination(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), count_termination_before_response)

    def test_accountant_cannot_update_termination(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.termination_list[0].name, self.termination_data["name"])

    def test_accountant_cannot_delete_termination(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.delete(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), count_termination_before_response)

    def test_ceo_can_view_termination_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_termination_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_termination(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Termination.objects.count(), count_termination_before_response + 1)

    def test_ceo_can_update_termination(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEquals(self.termination_list[0].name, self.termination_data["name"])

    def test_ceo_can_delete_termination(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.delete(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Termination.objects.count(), count_termination_before_response - 1)

    def test_hr_can_view_termination_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_termination_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_termination(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Termination.objects.count(), count_termination_before_response + 1)

    def test_hr_can_update_termination(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(self.termination_list[0].name, self.termination_data["name"])

    def test_hr_can_delete_termination(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.delete(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Termination.objects.count(), count_termination_before_response - 1)

    def test_manager_can_view_termination_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_termination_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_termination(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), count_termination_before_response)

    def test_manager_cannot_update_termination(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.put(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertNotEquals(self.termination_list[0].name, self.termination_data["name"])

    def test_manager_cannot_delete_termination(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_termination_before_response = Termination.objects.count()
        response = self.client.delete(
            reverse_lazy("termination-detail", kwargs={"pk": self.termination_list[0].id}), self.termination_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Termination.objects.count(), count_termination_before_response)

    def test_prevent_duplicate_termination_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.client.post(reverse_lazy("termination-list"), self.termination_data)
        self.assertRaises(serializers.ValidationError)
