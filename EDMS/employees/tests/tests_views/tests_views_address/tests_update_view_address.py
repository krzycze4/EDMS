from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import AddressFactory
from companies.models import Address
from django.urls import reverse_lazy
from users.factories import UserFactory


class AddressUpdateViewTests(EDMSTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.address = AddressFactory.create()
        self.employee = UserFactory.create()
        self.employee.address = self.address
        self.employee.save()
        update_address = AddressFactory.build()
        self.address_data = {
            "street_name": update_address.street_name,
            "street_number": update_address.street_number,
            "city": update_address.city,
            "postcode": update_address.postcode,
            "country": update_address.country,
        }
        self.view_url = reverse_lazy("update-employee-address", kwargs={"pk": self.employee.pk})
        self.not_logged_redirect_url = f"{reverse_lazy('login')}?next={self.view_url}"
        self.success_url = reverse_lazy("detail-employee", kwargs={"pk": self.employee.pk})
        self.template_name = "employees/addresses/address_update.html"

    def test_redirect_to_login_page_when_not_auth_user_execute_get_method(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_redirect_url)

    def test_redirect_to_login_page_when_not_auth_user_execute_post_method(self):
        response = self.client.post(self.view_url, data=self.address_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_redirect_url)

    def test_render_update_view_when_logged_user_group_accountants_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_address_when_logged_user_group_accountants_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.assertEqual(self.employee.address, self.address)
        response = self.client.post(self.view_url, data=self.address_data)
        expected_value = 1
        self.employee.refresh_from_db()
        self.assertEqual(Address.objects.count(), expected_value)
        self.assertEqual(self.employee.address.street_name, self.address_data["street_name"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_render_update_view_when_logged_user_group_ceos_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_address_when_logged_user_group_ceos_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.assertEqual(self.employee.address, self.address)
        response = self.client.post(self.view_url, data=self.address_data)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.address.street_name, self.address_data["street_name"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)

    def test_render_update_view_when_logged_user_group_managers_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_deny_update_address_when_logged_user_group_managers_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.assertEqual(self.employee.address, self.address)
        response = self.client.post(self.view_url, data=self.address_data)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.address, self.address)
        self.assertNotEquals(self.employee.address.street_name, self.address_data["street_name"])
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_render_update_view_when_logged_user_group_hrs_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_address_when_logged_user_group_hrs_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.assertEqual(self.employee.address, self.address)
        response = self.client.post(self.view_url, data=self.address_data)
        expected_value = 1
        self.assertEqual(Address.objects.count(), expected_value)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.address.street_name, self.address_data["street_name"])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.success_url)
