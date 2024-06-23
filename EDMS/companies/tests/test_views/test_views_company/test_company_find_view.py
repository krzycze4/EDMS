from http import HTTPStatus
from unittest.mock import patch

import requests
from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse, reverse_lazy

User = get_user_model()


class BaseCompanyFindTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
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

    def setUp(self) -> None:
        super().setUp()
        self.existing_company = CompanyFactory.create()


class CompanyFindViewTestsUserNotAuthenticated(BaseCompanyFindTestCase):
    def test_redirect_to_login_on_get(self):
        response = self.client.get(reverse_lazy("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('find-company')}")

    def test_redirect_to_login_on_post(self):
        response = self.client.post(reverse_lazy("find-company"), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, f"{reverse_lazy('login')}?next={reverse_lazy('find-company')}")


class CompanyFindViewTestsUserGroupAccountants(BaseCompanyFindTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_access_for_accountants(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("requests.get")
    def test_post_company_exists_in_db(self, mock_requests_get):
        self.assertTrue(self.login)
        mock_requests_get.return_value.status_code = HTTPStatus.OK
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.existing_company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company has already existed in the system!")

    def test_post_invalid_form(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": 1})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company doesn't exist! Insert correct KRS number.")

    @patch("requests.get")
    def test_post_timeout_api(self, mock_get):
        self.assertTrue(self.login)
        mock_get.side_effect = requests.Timeout
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Time limit for KRS request expired!")

    @patch("requests.get")
    def test_post_api_success(self, mock_get):
        self.assertTrue(self.login)
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = self.api_response_json
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("create-company"))
        self.assertDictEqual(self.client.session["company_data"], self.company_data)


class CompanyFindViewTestsUserGroupCeos(BaseCompanyFindTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_access_for_ceos(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("requests.get")
    def test_post_company_exists_in_db(self, mock_requests_get):
        self.assertTrue(self.login)
        mock_requests_get.return_value.status_code = HTTPStatus.OK
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.existing_company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company has already existed in the system!")

    def test_post_invalid_form(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": 1})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Company doesn't exist! Insert correct KRS number.")

    @patch("requests.get")
    def test_post_timeout_api(self, mock_get):
        self.assertTrue(self.login)
        mock_get.side_effect = requests.Timeout
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Time limit for KRS request expired!")

    @patch("requests.get")
    def test_post_api_success(self, mock_get):
        self.assertTrue(self.login)
        mock_get.return_value.status_code = HTTPStatus.OK
        mock_get.return_value.json.return_value = self.api_response_json
        response = self.client.post(reverse_lazy("find-company"), data={"krs_id": self.company.krs})
        self.assertTrue(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy("create-company"))
        self.assertDictEqual(self.client.session["company_data"], self.company_data)


class CompanyFindViewTestsUserGroupHrs(BaseCompanyFindTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_access_denied_for_hrs(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_access_denied_for_hrs(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class CompanyFindViewTestsUserGroupManagers(BaseCompanyFindTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_access_denied_for_managers(self):
        self.assertTrue(self.login)
        response = self.client.get(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_access_denied_for_managers(self):
        self.assertTrue(self.login)
        response = self.client.post(reverse("find-company"))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
