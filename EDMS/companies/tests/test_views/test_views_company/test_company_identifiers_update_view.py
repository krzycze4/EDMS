from http import HTTPStatus

from companies.factories import CompanyFactory
from companies.models import Company
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseCompanyIdentifiersUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        group_names_with_permission_codenames = {
            "ceos": [
                "add_company",
                "change_company",
                "delete_company",
                "view_company",
            ],
            "accountants": ["add_company", "change_company", "delete_company", "view_company"],
            "managers": ["view_company"],
            "hrs": ["view_company"],
        }
        for (group_name, permission_codenames) in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)

        cls.password = User.objects.make_random_password()
        cls.accountant = cls.create_user_with_group(group_name="accountants")
        cls.ceo = cls.create_user_with_group(group_name="ceos")
        cls.hr = cls.create_user_with_group(group_name="hrs")
        cls.manager = cls.create_user_with_group(group_name="managers")
        cls.template_name = "companies/companies/update_identifiers_company.html"

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.company = CompanyFactory.create()
        company_stub = CompanyFactory.stub()
        self.company_data = {
            "name": company_stub.name,
            "krs": company_stub.krs,
            "regon": company_stub.regon,
            "nip": company_stub.nip,
            "shortcut": company_stub.shortcut,
            "is_mine": company_stub.is_mine,
        }
        self.not_auth_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('update-identifiers', kwargs={'pk': self.company.pk})}"
        )
        self.redirect_url = f"{reverse_lazy('detail-company', kwargs={'pk': self.company.pk})}"


class TestCaseCompanyIdentifiersUpdateViewUserNotAuthenticated(TestCaseCompanyIdentifiersUpdateView):
    def test_get_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_post_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)


class TestCaseCompanyIdentifiersUpdateViewUserGroupAccountants(TestCaseCompanyIdentifiersUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Company.objects.get(pk=self.company.pk).name, self.company_data["name"])

    def test_post_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)


class TestCaseCompanyIdentifiersUpdateViewUserGroupCeos(TestCaseCompanyIdentifiersUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Company.objects.get(pk=self.company.pk).name, self.company_data["name"])

    def test_post_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)


class TestCaseCompanyIdentifiersUpdateViewUserGroupHrs(TestCaseCompanyIdentifiersUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_user_hrs_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_user_hrs_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseCompanyIdentifiersUpdateViewUserGroupManagers(TestCaseCompanyIdentifiersUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
