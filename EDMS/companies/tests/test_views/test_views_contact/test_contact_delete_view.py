from http import HTTPStatus

from companies.factories import CompanyFactory, ContactFactory
from companies.models import Contact
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseContactDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        cls.accountant = cls.create_user_with_group(group_name="accountants")
        cls.ceo = cls.create_user_with_group(group_name="ceos")
        cls.hr = cls.create_user_with_group(group_name="hrs")
        cls.manager = cls.create_user_with_group(group_name="managers")

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.create(company=self.company)
        self.not_logged_user_url = f"{reverse_lazy('login')}?next={reverse_lazy('delete-contact', kwargs={'company_pk': self.company.pk, 'contact_pk': self.contact.pk})}"


class TestCaseContactDeleteViewUserNotAuthenticated(TestCaseContactDeleteView):
    def test_get_method_when_user_not_authenticated(self):
        response = self.client.get(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_post_method_when_user_not_authenticated(self):
        response = self.client.post(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)


class TestCaseCompanyDeleteViewUserGroupAccountants(TestCaseContactDeleteView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter - 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))


class TestCaseCompanyDeleteViewUserGroupCeos(TestCaseContactDeleteView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter - 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))


class TestCaseCompanyDeleteViewUserGroupHrs(TestCaseContactDeleteView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter - 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))


class TestCaseCompanyDeleteViewUserGroupManagers(TestCaseContactDeleteView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("delete-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter - 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
