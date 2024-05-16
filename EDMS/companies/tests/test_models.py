from companies.factories import AddressFactory, CompanyFactory, ContactFactory
from companies.models import Address, Company, Contact
from django.test import TestCase


class TestCaseAddress(TestCase):
    def setUp(self) -> None:
        self.address = AddressFactory.build()

    def test_save_address_in_db(self):
        self.address.save()
        self.assertEqual(Address.objects.count(), 1)

    def test_return_str(self):
        expected_str = f"{self.address.street_name} {self.address.street_number}\n{self.address.postcode} {self.address.city}\n{self.address.country}"
        self.assertEqual(str(self.address), expected_str)

    def test_verbose_name_plural(self):
        self.assertEqual(Address._meta.verbose_name_plural, "Addresses")


class TestCaseCompany(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory.build()
        self.company.address.save()

    def test_save_company_in_db(self):
        self.company.save()
        self.assertTrue(Company.objects.count(), 1)

    def test_return_str(self):
        self.assertEqual(f"{self.company.name}", str(self.company))

    def test_verbose_name_plural(self):
        self.assertEqual(Company._meta.verbose_name_plural, "Companies")


class TestCaseContact(TestCase):
    def setUp(self) -> None:
        self.contact = ContactFactory.build()
        self.contact.company.address.save()
        self.contact.company.save()

    def test_save_contact_in_db(self):
        self.contact.save()
        self.assertEqual(Contact.objects.count(), 1)

    def test_return_str(self):
        self.assertEqual(f"{self.contact.name}", str(self.contact))
