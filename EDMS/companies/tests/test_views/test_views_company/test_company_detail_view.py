from http import HTTPStatus

from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseCompanyDetailView(TestCase):
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

        cls.company = CompanyFactory.create()
        cls.not_auth_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('detail-company', kwargs={'pk': cls.company.pk})}"
        )

        cls.template_name = "companies/companies/detail_company.html"

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user


class TestCaseGetCompanyDetailView(TestCaseCompanyDetailView):
    def test_get_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_get_user_group_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_group_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_group_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_group_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
