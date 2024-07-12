from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory, ContactFactory
from companies.models import Contact
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ContactCreateTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "companies/contacts/create_contact.html"

    def setUp(self) -> None:
        super().setUp()
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.create(company=self.company)
        self.contact_stub = ContactFactory.stub(company=self.company)
        self.contact_data = {
            "name": self.contact_stub.name,
            "email": self.contact_stub.email,
            "phone": self.contact_stub.phone,
            "description": self.contact_stub.description,
            "company": self.company.pk,
        }
        self.not_logged_user_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('create-contact', kwargs={'pk': self.company.pk})}"
        )

    def test_redirect_to_login_on_get_when_user_not_authenticated(self):
        response = self.client.get(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_on_post_when_user_not_authenticated(self):
        response = self.client.post(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}), data={})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_render_create_contact_view_for_accountants_when_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_contact_and_redirect_for_accountants_when_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("create-contact", kwargs={"pk": self.company.pk}), data=self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter + 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_create_contact_view_for_ceos_when_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_contact_and_redirect_for_ceos_when_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("create-contact", kwargs={"pk": self.company.pk}), data=self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter + 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_create_contact_view_for_hrs_when_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_contact_and_redirect_for_hrs_when_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("create-contact", kwargs={"pk": self.company.pk}), data=self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter + 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_create_contact_view_for_managers_when_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(reverse_lazy("create-contact", kwargs={"pk": self.company.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_create_contact_and_redirect_for_managers_when_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("create-contact", kwargs={"pk": self.company.pk}), data=self.contact_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter + 1)
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
