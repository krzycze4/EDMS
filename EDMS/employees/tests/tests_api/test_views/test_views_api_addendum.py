from http import HTTPStatus
from typing import List

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_addendum import Addendum
from rest_framework import serializers
from rest_framework.test import APIClient

User = get_user_model()


class AddendumApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.addendum_list: List[Addendum] = AddendumFactory.create_batch(9)
        agreement = AgreementFactory.create()
        self.addendum: Addendum = AddendumFactory.build(agreement=agreement)
        self.addendum_data = {
            "name": self.addendum.name,
            "agreement": agreement.id,
            "create_date": self.addendum.create_date,
            "end_date": self.addendum.end_date,
            "salary_gross": self.addendum.salary_gross,
            "scan": self.addendum.scan,
        }

    def test_unauthenticated_user_cannot_view_addendum_list(self):
        response = self.client.get(reverse_lazy("addendum-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_addendum_detail(self):
        response = self.client.get(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_addendum(self):
        response = self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_addendum(self):
        response = self.client.put(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_addendum(self):
        response = self.client.delete(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_accountant_can_view_addendum_list(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_addendum_detail(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_cannot_create_addendum(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_accountant_cannot_update_addendum(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.put(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_accountant_cannot_delete_addendum(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Addendum.objects.count()
        response = self.client.delete(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_address_before_response)

    def test_ceo_can_view_addendum_list(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_addendum_detail(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_addendum(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response + 1)

    def test_ceo_can_update_addendum(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.put(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_ceo_can_delete_addendum(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.delete(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response - 1)

    def test_hr_can_view_addendum_list(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_addendum_detail(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_addendum(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response + 1)

    def test_hr_can_update_addendum(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.put(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_hr_can_delete_addendum(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.delete(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response - 1)

    def test_manager_can_view_addendum_list(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_addendum_detail(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_cannot_create_addendum(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_manager_cannot_update_addendum(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_addendum_before_response = Addendum.objects.count()
        response = self.client.put(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_addendum_before_response)

    def test_manager_cannot_delete_addendum(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        count_address_before_response = Addendum.objects.count()
        response = self.client.delete(
            reverse_lazy("addendum-detail", kwargs={"pk": self.addendum_list[0].id}), self.addendum_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Addendum.objects.count(), count_address_before_response)

    def test_prevent_duplicate_addendum_creation(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.client.post(reverse_lazy("addendum-list"), self.addendum_data)
        self.assertRaises(serializers.ValidationError)
