# class TestCompaniesFactories(TestCase):
#     def test_create_correct_object(self):
#         FactoryXyz.create()
#
#         self.assertEqual(Object.objects.count(), 1)
#
#     def test_create_correct_object_bulk(self):
#         FactoryXyz.create_batch(10)
#
#         self.assertEqual(Object.objects.count(), 10)
from companies.factories import AddressFactory, CompanyFactory, ContactFactory
from companies.models import Address, Company, Contact
from django.test import TestCase


class TestAddressFactory(TestCase):
    def test_create_correct_address(self):
        AddressFactory.create()
        self.assertEqual(Address.objects.count(), 1)

    def test_create_correct_address_bulk(self):
        AddressFactory.create_batch(10)
        self.assertEqual(Address.objects.count(), 10)


class TestCompanyFactory(TestCase):
    def test_create_correct_company(self):
        CompanyFactory.create()
        self.assertEqual(Company.objects.count(), 1)

    def test_create_correct_company_bulk(self):
        CompanyFactory.create_batch(10)
        self.assertEqual(Company.objects.count(), 10)


class TestContactFactory(TestCase):
    def test_create_correct_contact(self):
        ContactFactory.create()
        self.assertEqual(Contact.objects.count(), 1)

    def test_create_correct_contact_bulk(self):
        ContactFactory.create_batch(10)
        self.assertEqual(Contact.objects.count(), 10)
