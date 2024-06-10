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


class TestCaseCompanyCreateView(TestCase):
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

        cls.template_name = "companies/companies/list_company.html"

        # cls.company = CompanyFactory.build()
        # cls.company_session_data = {
        #     "name": company.name,
        #     "krs": company.krs,
        #     "regon": company.regon,
        #     "nip": company.nip,
        #     "street_name": company.address.street_name,
        #     "street_number": company.address.street_number,
        #     "city": company.address.city,
        #     "postcode": company.address.postcode,
        #     "country": company.address.country,
        #     "shortcut": company.shortcut,
        # }

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.company_list = CompanyFactory.create_batch(11)


class TestCaseGetCompanyListViewUserNotAuthenticated(TestCaseCompanyCreateView):
    def test_get_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('list-company')}")


class TestCaseGetCompanyListViewUserGroupAccountants(TestCaseCompanyCreateView):
    def setUp(self):
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_user_group_accountants_page_1(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_user_group_accountants_page_2(self):
        self.assertTrue(self.login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_get_user_group_accountants_filter(self):
        self.assertTrue(self.login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")


class TestCaseGetCompanyListViewUserGroupCeos(TestCaseCompanyCreateView):
    def setUp(self):
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_user_group_ceos_page_1(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_user_group_ceos_page_2(self):
        self.assertTrue(self.login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_get_user_group_ceos_filter(self):
        self.assertTrue(self.login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")


class TestCaseGetCompanyListViewUserGroupHrs(TestCaseCompanyCreateView):
    def setUp(self):
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_user_group_hrs_page_1(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_user_group_hrs_page_2(self):
        self.assertTrue(self.login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_get_user_group_hrs_filter(self):
        self.assertTrue(self.login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")


class TestCaseGetCompanyListViewUserGroupManagers(TestCaseCompanyCreateView):
    def setUp(self):
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_user_group_managers_page_1(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("list-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 10)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")

    def test_get_user_group_managers_page_2(self):
        self.assertTrue(self.login)
        response = self.client.get(f"{reverse_lazy('list-company')}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 2 of 2>")

    def test_get_user_group_managers_filter(self):
        self.assertTrue(self.login)
        response = self.client.get(
            f"{reverse_lazy('list-company')}?name__icontains={self.company_list[0].name}&krs=&regon=&nip=&shortcut__icontains="
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertEqual(len(response.context["companies"]), 1)
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 1>")
