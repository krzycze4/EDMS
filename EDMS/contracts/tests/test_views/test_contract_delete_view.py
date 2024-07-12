from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ContractDeleteViewTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.contract = ContractFactory.create()
        cls.not_auth_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('delete-contract', kwargs={'pk': cls.contract.pk})}"
        )
        cls.template_name = "contracts/contract_delete.html"

    def test_redirect_to_login_on_get_when_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_redirect_to_login_on_post_when_user_not_authenticated(self):
        response = self.client.post(
            reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_auth_user_url)

    def test_denied_access_for_accountants_when_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.get(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)

    def test_denied_access_and_not_delete_contract_for_accountants_when_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)

    def test_render_delete_contract_view_for_ceos_when_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_delete_contact_and_redirect_for_ceos_when_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contract.objects.count(), contract_counter - 1)
        self.assertRedirects(response, reverse_lazy("list-contract"))

    def test_denied_access_for_hrs_when_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.get(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)

    def test_denied_access_and_not_delete_contract_for_hrs_when_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)

    def test_denied_access_for_managers_when_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.get(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)

    def test_denied_access_and_not_delete_contract_for_managers_when_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contract_counter = Contract.objects.count()
        response = self.client.post(reverse_lazy("delete-contract", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(Contract.objects.count(), contract_counter)
