from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from companies.factories import CompanyFactory, ContactFactory
from companies.models import Contact
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class ContactUpdateViewTestCase(EDMSTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.template_name = "companies/contacts/update_contact.html"

    def setUp(self) -> None:
        super().setUp()
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.create(company=self.company)
        self.contact_stub = ContactFactory.stub(company=self.company)
        self.existing_contact_data = {
            "name": self.contact.name,
            "email": self.contact.email,
            "phone": self.contact.phone,
            "description": self.contact.description,
            "company": self.company.id,
        }
        self.new_contact_data = {
            "name": self.contact_stub.name,
            "email": self.contact_stub.email,
            "phone": self.contact_stub.phone,
            "description": self.contact_stub.description,
            "company": self.company.id,
        }
        self.not_logged_user_url = f"{reverse_lazy('login')}?next={reverse_lazy('update-contact', kwargs={'company_pk': self.company.pk, 'contact_pk': self.contact.pk})}"

    def test_redirect_to_login_on_get_when_user_not_authenticated(self):
        response = self.client.get(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_redirect_to_login_on_post_when_user_not_authenticated(self):
        response = self.client.post(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data={},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.not_logged_user_url)

    def test_render_update_contact_view_for_accountants_when_execute_get_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_contact_and_redirect_for_accountants_when_execute_post_method(self):
        login = self.client.login(email=self.accountant.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data=self.new_contact_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, self.new_contact_data["name"])
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_update_contact_view_for_ceos_when_execute_get_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_contact_and_redirect_for_ceos_when_execute_post_method(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data=self.new_contact_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, self.new_contact_data["name"])
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_update_contact_view_for_hrs_when_execute_get_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_update_contact_and_redirect_for_hrs_when_execute_post_method(self):
        login = self.client.login(email=self.hr.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data=self.new_contact_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, self.new_contact_data["name"])
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))

    def test_render_update_contact_view_for_managers_when_execute_get_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        response = self.client.get(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)

    def test_update_contact_and_redirect_for_managers_when_execute_post_method(self):
        login = self.client.login(email=self.manager.email, password=self.password)
        self.assertTrue(login)
        contact_counter = Contact.objects.count()
        response = self.client.post(
            reverse_lazy("update-contact", kwargs={"company_pk": self.company.pk, "contact_pk": self.contact.pk}),
            data=self.new_contact_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Contact.objects.count(), contact_counter)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, self.new_contact_data["name"])
        self.assertRedirects(response, reverse_lazy("detail-company", kwargs={"pk": self.company.pk}))
