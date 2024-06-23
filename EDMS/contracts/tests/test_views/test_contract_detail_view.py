from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from contracts.factories import ContractFactory
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ContractDetailViewTests(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.contract = ContractFactory.create()
        cls.not_auth_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('detail-contract', kwargs={'pk': cls.contract.pk})}"
        )
        cls.template_name = "contracts/contract_detail.html"

    def test_redirect_if_user_is_not_authenticated(self):
        response = self.client.get(reverse_lazy("detail-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_access_for_accountants(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_access_for_ceos(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_access_for_hrs(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_access_for_managers(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("detail-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
