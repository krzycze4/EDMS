from http import HTTPStatus

from companies.factories import AddressFactory, CompanyFactory, ContactFactory
from companies.models import Contact
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import serializers
from rest_framework.test import APIClient
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseContactModelViewSet(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        group_names_with_permission_codenames = {
            "ceos": [
                "add_contact",
                "change_contact",
                "delete_contact",
                "view_contact",
            ],
            "accountants": [
                "add_contact",
                "change_contact",
                "delete_contact",
                "view_contact",
            ],
            "managers": [
                "add_contact",
                "change_contact",
                "delete_contact",
                "view_contact",
            ],
            "hrs": [
                "add_contact",
                "change_contact",
                "delete_contact",
                "view_contact",
            ],
        }
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

        cls.password = User.objects.make_random_password()
        cls.user_address = AddressFactory.create()

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

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password, address=cls.user_address)
        user.groups.add(group)
        return user


class TestCaseUserNotAuthenticatedContactModelViewSet(TestCaseContactModelViewSet):
    def test_get_list_contact_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_detail_contact_if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_create_contact_if_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_put_update_contact_if_user_not_authenticated(self):
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_contact_if_user_not_authenticated(self):
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseUserAccountantContactModelViewSet(TestCaseContactModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.accountant = self.create_user_with_group(group_name="accountants")
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_list_contact_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_contact_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_contact_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), 11)

    def test_put_update_contact_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), 10)

    def test_delete_contact_if_user_group_accountant(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 9)


class TestCaseUserCeoContactModelViewSet(TestCaseContactModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_list_contact_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_contact_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_contact_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), 11)

    def test_put_update_contact_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), 10)

    def test_delete_contact_if_user_group_ceo(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 9)


class TestCaseUserHrContactModelViewSet(TestCaseContactModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.hr = self.create_user_with_group(group_name="hrs")
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_list_contact_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_contact_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_contact_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), 11)

    def test_put_update_contact_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), 10)

    def test_delete_contact_if_user_group_hr(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 9)


class TestCaseUserManagerContactModelViewSet(TestCaseContactModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.manager = self.create_user_with_group(group_name="hrs")
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_list_contact_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_detail_contact_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_contact_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Contact.objects.count(), 11)

    def test_put_update_contact_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.put(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Contact.objects.count(), 10)

    def test_delete_contact_if_user_group_manager(self):
        self.assertTrue(self.login)
        response = self.client.delete(
            reverse_lazy("contact-detail", kwargs={"pk": self.contact_list[0].id}), self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 9)


class TestCaseCreateInstanceContactModelViewSet(TestCaseContactModelViewSet):
    def setUp(self) -> None:
        super().setUp()
        self.ceo = self.create_user_with_group(group_name="ceos")
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_not_create_same_contact(self):
        self.assertTrue(self.login)
        self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.client.post(reverse_lazy("contact-list"), self.contact_data)
        self.assertEqual(Contact.objects.count(), 11)
        self.assertRaises(serializers.ValidationError)
