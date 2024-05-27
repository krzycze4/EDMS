from http import HTTPStatus
from unittest.mock import patch

import requests
from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class TestCaseCompanyFindView(TestCase):
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

        cls.password = "default_password"
        cls.company = CompanyFactory.stub()
        cls.api_response_json = {
            "odpis": {
                "dane": {
                    "dzial1": {
                        "danePodmiotu": {
                            "nazwa": cls.company.name,
                            "identyfikatory": {"regon": cls.company.regon, "nip": cls.company.nip},
                        },
                        "siedzibaIAdres": {
                            "adres": {
                                "ulica": cls.company.address.street_name,
                                "nrDomu": cls.company.address.street_number,
                                "miejscowosc": cls.company.address.city,
                                "kodPocztowy": cls.company.address.postcode,
                                "kraj": cls.company.address.country,
                            }
                        },
                    }
                }
            }
        }
        cls.company_data = {
            "name": cls.company.name,
            "krs": str(cls.company.krs),
            "regon": cls.company.regon,
            "nip": cls.company.nip,
            "street_name": cls.company.address.street_name,
            "street_number": cls.company.address.street_number,
            "city": cls.company.address.city,
            "postcode": cls.company.address.postcode,
            "country": cls.company.address.country,
        }
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
        self.existing_company = CompanyFactory.create()


class TestCaseCompanyFindViewUserNotAuthenticated(TestCaseCompanyFindView):
    def test_get_method_when_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('find-company')}")

    def test_post_method_when_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("find-company"), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('find-company')}")


class TestCaseCompanyFindViewUserGroupAccountants(TestCaseCompanyFindView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_method_when_user_group_is_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("requests.get")
    def test_post_method_when_user_group_is_accountants_if_company_exists_in_db(self, mock_requests_get):
        self.assertTrue(self.login)
        mock_requests_get.return_value.status_code = HTTPStatus.OK
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.existing_company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company has already existed in the system!")

    def test_post_method_when_user_group_is_accountants_if_form_invalid(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": 1})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company doesn't exist! Insert correct KRS number.")

    @patch("requests.get")
    def test_post_method_when_user_group_is_accountants_if_timeout_api(self, mock_get):
        self.assertTrue(self.login)
        mock_get.side_effect = requests.Timeout
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Time limit for KRS request expired!")

    @patch("requests.get")
    def test_post_method_when_user_group_is_accountants_if_api_success(self, mock_get):
        self.assertTrue(self.login)
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = self.api_response_json
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("create-company"))
        self.assertDictEqual(self.client.session["company_data"], self.company_data)


class TestCaseCompanyFindViewUserGroupCeos(TestCaseCompanyFindView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_method_when_user_group_is_ceos(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("requests.get")
    def test_post_method_when_user_group_is_ceos_if_company_exists_in_db(self, mock_requests_get):
        self.assertTrue(self.login)
        mock_requests_get.return_value.status_code = HTTPStatus.OK
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.existing_company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company has already existed in the system!")

    def test_post_method_when_user_group_is_ceos_if_form_invalid(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": 1})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company doesn't exist! Insert correct KRS number.")

    @patch("requests.get")
    def test_post_method_when_user_group_is_ceos_if_timeout_api(self, mock_get):
        self.assertTrue(self.login)
        mock_get.side_effect = requests.Timeout
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Time limit for KRS request expired!")

    @patch("requests.get")
    def test_post_method_when_user_group_is_ceos_if_api_success(self, mock_get):
        self.assertTrue(self.login)
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = self.api_response_json
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("create-company"))
        self.assertDictEqual(self.client.session["company_data"], self.company_data)


class TestCaseCompanyFindViewUserGroupHrs(TestCaseCompanyFindView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_method_when_user_group_is_hrs(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_method_when_user_group_is_hrs(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCaseCompanyFindViewUserGroupManagers(TestCaseCompanyFindView):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_method_when_user_group_is_managers(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_method_when_user_group_is_managers(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
