from http import HTTPStatus

from companies.factories import AddressFactory, CompanyFactory
from companies.models import Address
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse_lazy
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseCompanyAddressUpdateView(TestCase):
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
        cls.template_name = "companies/companies/update_address_company.html"

    @classmethod
    def create_user_with_group(cls, group_name: str) -> User:
        group = get_object_or_404(Group, name=group_name)
        user = UserFactory(is_active=True, password=cls.password)
        user.groups.add(group)
        return user

    def setUp(self) -> None:
        self.company = CompanyFactory.create()
        address_stub = AddressFactory.stub()
        self.address_data = {
            "street_name": address_stub.street_name,
            "street_number": address_stub.street_number,
            "city": address_stub.city,
            "postcode": address_stub.postcode,
            "country": address_stub.country,
        }
        self.not_auth_user_url = f"{reverse_lazy('login')}?next={reverse_lazy('update-address', kwargs={'company_pk': self.company.pk, 'address_pk': self.company.address.pk})}"
        self.redirect_url = f"{reverse_lazy('detail-company', kwargs={'pk': self.company.pk})}"


class TestCaseCompanyAddressUpdateViewUserNotAuthenticated(TestCaseCompanyAddressUpdateView):
    def test_get_user_not_authenticated(self):
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_post_user_not_authenticated(self):
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)


class TestCaseCompanyAddressUpdateViewUserGroupAccountants(TestCaseCompanyAddressUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        with self.assertRaises(Address.DoesNotExist):
            self.client.get(reverse_lazy("update-address", kwargs={"company_pk": self.company.pk, "address_pk": 100}))

    def test_post_user_accountants_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Address.objects.get(pk=self.company.address.pk).street_name, self.address_data["street_name"])

    def test_post_user_accountants_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)


class TestCaseCompanyAddressUpdateViewUserGroupCeos(TestCaseCompanyAddressUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_user_ceos_ok(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_user_ceos_not_ok(self):
        self.assertTrue(self.login)
        with self.assertRaises(Address.DoesNotExist):
            self.client.get(reverse_lazy("update-address", kwargs={"company_pk": self.company.pk, "address_pk": 100}))

    def test_post_user_ceos_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Address.objects.get(pk=self.company.address.pk).street_name, self.address_data["street_name"])

    def test_post_user_ceos_not_ok(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)


class TestCaseCompanyAddressUpdateViewUserGroupHrs(TestCaseCompanyAddressUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseCompanyAddressUpdateViewUserGroupManagers(TestCaseCompanyAddressUpdateView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_user_managers_forbidden(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
