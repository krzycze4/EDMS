from companies.factories import CompanyFactory, ContactFactory
from companies.forms.forms_contact import CreateContactForm, UpdateContactForm
from django.test import TestCase


class CreateContactFormTests(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.build(company=self.company)
        self.existing_contact = ContactFactory.create(company=self.company)

    def test_form_valid(self):
        form = CreateContactForm(
            data={
                "name": self.contact.name,
                "email": self.contact.email,
                "phone": self.contact.phone,
                "description": self.contact.description,
                "company": self.company,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_the_same_contact_exists_in_db(self):
        form = CreateContactForm(
            data={
                "name": self.existing_contact.name,
                "email": self.existing_contact.email,
                "phone": self.existing_contact.phone,
                "description": self.contact.description,
                "company": self.company,
            }
        )
        self.assertFalse(form.is_valid())


class UpdateContactFormTests(TestCase):
    def setUp(self) -> None:
        self.contact = ContactFactory.create()
        self.new_contact = ContactFactory.build()

    def test_form_valid(self):
        form = UpdateContactForm(
            instance=self.contact,
            data={
                "name": self.new_contact.name,
                "email": self.new_contact.email,
                "phone": self.new_contact.phone,
                "description": self.new_contact.description,
                "company": self.contact.company,
            },
        )
        self.assertTrue(form.is_valid())
