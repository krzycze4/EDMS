from companies.factories import CompanyFactory, ContactFactory
from companies.forms.forms_contact import CreateContactForm, UpdateContactForm
from django.test import TestCase


class TestCaseCreateContactForm(TestCase):
    def setUp(self) -> None:
        self.contact = ContactFactory.build()
        self.company = CompanyFactory.create()

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


class TestCaseUpdateContactForm(TestCase):
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
        print(form.errors)
        self.assertTrue(form.is_valid())
