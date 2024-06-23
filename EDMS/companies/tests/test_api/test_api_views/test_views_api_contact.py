from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory, ContactFactory
from companies.models import Contact
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient

User = get_user_model()


class BaseContactApiTestCase(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.contact_list = ContactFactory.create_batch(10)
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.stub()
        self.contact_data = {
            "name": self.contact.name,
            "email": self.contact.email,
            "phone": self.contact.phone,
            "description": self.contact.description,
            "company": self.company.id,
        }


class UnauthenticatedUserApiContactTests(BaseContactApiTestCase):
    def test_unauthenticated_user_cannot_view_contact_list(self):
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_view_contact_detail(self):
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_create_contact(self):
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_update_contact(self):
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_contact(self):
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class AccountantApiContactTests(BaseContactApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_accountant_can_view_contact_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_view_contact_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_accountant_can_create_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), count_company_before_response + 1)

    def test_accountant_can_update_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), count_company_before_response)

    def test_accountant_can_delete_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), count_company_before_response - 1)


class CeoApiContactTests(BaseContactApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_ceo_can_view_contact_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_view_contact_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ceo_can_create_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), count_company_before_response + 1)

    def test_ceo_can_update_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), count_company_before_response)

    def test_ceo_can_delete_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), count_company_before_response - 1)


class HrApiContactTests(BaseContactApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_hr_can_view_contact_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_view_contact_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_hr_can_create_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), count_company_before_response + 1)

    def test_hr_can_update_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), count_company_before_response)

    def test_hr_can_delete_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), count_company_before_response - 1)


class ManagerApiContactTests(BaseContactApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_manager_can_view_contact_list(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_view_contact_detail(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_manager_can_create_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), count_company_before_response + 1)

    def test_manager_can_update_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), count_company_before_response)

    def test_manager_can_delete_contact(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), count_company_before_response - 1)


class CreateInstanceApiContactTests(BaseContactApiTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_prevent_duplicate_contact_creation(self):
        self.assertTrue(self.login)
        count_company_before_response = Contact.objects.count()
        self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(Contact.objects.count(), count_company_before_response + 1)
        self.assertRaises(serializers.ValidationError)
