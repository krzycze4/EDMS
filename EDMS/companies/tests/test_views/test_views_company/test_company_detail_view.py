from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class CompanyDetailViewTests(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.company = CompanyFactory.create()
        cls.not_auth_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('detail-company', kwargs={'pk': cls.company.pk})}"
        )
        cls.template_name = "companies/companies/detail_company.html"

    def test_redirect_if_user_is_not_authenticated(self):
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_access_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_access_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_access_for_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_access_for_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
