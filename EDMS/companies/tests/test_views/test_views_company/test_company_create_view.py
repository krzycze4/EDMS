from http import HTTPStatus

from companies.factories import CompanyFactory
from companies.models import Address, Company
from companies.views.views_company import CompanyCreateView
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

        company = CompanyFactory.build()
        cls.company_session_data = {
            "name": company.name,
            "krs": company.krs,
            "regon": company.regon,
            "nip": company.nip,
            "street_name": company.address.street_name,
            "street_number": company.address.street_number,
            "city": company.address.city,
            "postcode": company.address.postcode,
            "country": company.address.country,
            "shortcut": company.shortcut,
        }

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.company = CompanyFactory.build()
        session = self.client.session
        session["company_data"] = self.company_session_data
        session.save()


class TestCaseCompanyCreateViewUserNotAuthenticated(TestCaseCompanyCreateView):
    def test_get_method_when_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('create-company')}")

    def test_post_method_when_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("create-company"), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('create-company')}")


class TestCaseCompanyCreateViewUserGroupAccountants(TestCaseCompanyCreateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_correct_initials(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        view = CompanyCreateView()
        view.request = response.wsgi_request
        initial = view.get_initial()
        self.assertEqual(initial, self.company_session_data)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        company_counter = Company.objects.count()
        address_counter = Address.objects.count()
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Company.objects.count(), company_counter + 1)
        self.assertEqual(Address.objects.count(), address_counter + 1)
        self.assertRedirects(response, reverse_lazy("create-company-done"))


class TestCaseCompanyCreateViewUserGroupCeos(TestCaseCompanyCreateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_correct_initials(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        view = CompanyCreateView()
        view.request = response.wsgi_request
        initial = view.get_initial()
        self.assertEqual(initial, self.company_session_data)

    def test_get_method_when_user_group_is_ceos(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_when_user_group_is_ceos(self):
        self.assertTrue(self.login)
        company_counter = Company.objects.count()
        address_counter = Address.objects.count()
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Company.objects.count(), company_counter + 1)
        self.assertEqual(Address.objects.count(), address_counter + 1)
        self.assertRedirects(response, reverse_lazy("create-company-done"))


class TestCaseCompanyCreateViewUserGroupHrs(TestCaseCompanyCreateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_method_when_user_group_is_hrs(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_method_when_user_group_is_hrs(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseCompanyCreateViewUserGroupManagers(TestCaseCompanyCreateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_method_when_user_group_is_managers(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse_lazy("create-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_method_when_user_group_is_managers(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("create-company"), data=self.company_session_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
