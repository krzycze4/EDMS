from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import AddressFactory, CompanyFactory
from companies.models import Address, Company
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class BaseAddressTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "companies/companies/update_address_company.html"

    def setUp(self) -> None:
        super().setUp()
        self.company: Company = CompanyFactory.create()
        address_stub: Address = AddressFactory.stub()
        self.address_data = {
            "street_name": address_stub.street_name,
            "street_number": address_stub.street_number,
            "city": address_stub.city,
            "postcode": address_stub.postcode,
            "country": address_stub.country,
        }
        self.not_auth_user_url = f"{reverse_lazy('login')}?next={reverse_lazy('update-address', kwargs={'company_pk': self.company.pk, 'address_pk': self.company.address.pk})}"
        self.redirect_url = f"{reverse_lazy('detail-company', kwargs={'pk': self.company.pk})}"


class UnauthenticatedUserAddressUpdateTests(BaseAddressTestCase):
    def test_redirect_to_login_on_get_when_not_authenticated(self):
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_redirect_to_login_when_not_authenticated_user_post(self):
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)


class AccountantAddressUpdateTests(BaseAddressTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.accountant.email, password=self.password)

    def test_get_address_update_page_for_accountant(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_not_existing_address_for_accountant(self):
        self.assertTrue(self.login)
        with self.assertRaises(Address.DoesNotExist):
            self.client.get(reverse_lazy("update-address", kwargs={"company_pk": self.company.pk, "address_pk": 100}))

    def test_post_correct_address_update_for_accountant(self):
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

    def test_post_invalid_address_update_for_accountant(self):
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


class CeoAddressUpdateTests(BaseAddressTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.ceo.email, password=self.password)

    def test_get_address_update_page_for_ceo(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_not_existing_address_for_ceo(self):
        self.assertTrue(self.login)
        with self.assertRaises(Address.DoesNotExist):
            self.client.get(reverse_lazy("update-address", kwargs={"company_pk": self.company.pk, "address_pk": 100}))

    def test_post_correct_address_update_for_ceo(self):
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

    def test_post_invalid_address_update_for_ceo(self):
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


class HrAddressUpdateTests(BaseAddressTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.hr.email, password=self.password)

    def test_get_address_update_forbidden_for_hr(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_address_update_forbidden_for_hr(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class ManagerAddressUpdateTests(BaseAddressTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.login = self.client.login(email=self.manager.email, password=self.password)

    def test_get_address_update_forbidden_for_manager(self):
        self.assertTrue(self.login)
        response = self.client.get(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_address_update_forbidden_for_manager(self):
        self.assertTrue(self.login)
        response = self.client.post(
            reverse_lazy(
                "update-address", kwargs={"company_pk": self.company.pk, "address_pk": self.company.address.pk}
            ),
            data=self.address_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
