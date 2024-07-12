from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from companies.models import Company
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class CompanyIdentifiersUpdateTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "companies/companies/update_identifiers_company.html"

    def setUp(self) -> None:
        super().setUp()
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
        self.not_authenticated_redirect_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('update-identifiers', kwargs={'pk': self.company.pk})}"
        )
        self.success_redirect_url = f"{reverse_lazy('detail-company', kwargs={'pk': self.company.pk})}"

    def test_get_redirects_to_login(self):
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_authenticated_redirect_url)

    def test_post_redirects_to_login(self):
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_authenticated_redirect_url)

    def test_get_accountants_access_ok(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_accountants_access_not_found(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_accountants_updates_company_ok(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_redirect_url)
        self.assertEqual(Company.objects.get(pk=self.company.pk).name, self.company_data["name"])

    def test_post_accountants_validation_errors(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)

    def test_get_ceos_access_ok(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_get_ceos_access_not_found(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_ceos_updates_company_ok(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_redirect_url)
        self.assertEqual(Company.objects.get(pk=self.company.pk).name, self.company_data["name"])

    def test_post_ceos_validation_errors(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        self.assertTrue(response.context["form"].errors)

    def test_get_hrs_access_forbidden(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_hrs_access_forbidden(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_get_managers_access_forbidden(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_post_managers_access_forbidden(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.post(
            reverse_lazy("update-identifiers", kwargs={"pk": self.company.pk}), data=self.company_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
