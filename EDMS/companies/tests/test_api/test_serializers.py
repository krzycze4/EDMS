from companies.api.serializers import (
    AddressSerializer,
    CompanySerializer,
    ContactSerializer,
)
from companies.factories import AddressFactory, CompanyFactory, ContactFactory
from companies.models import Address, Company, Contact
from django.test import TestCase


class AddressSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.address = AddressFactory.build()
        self.address_data = {
            "id": self.address.id,
            "street_name": self.address.street_name,
            "street_number": str(self.address.street_number),
            "city": self.address.city,
            "postcode": self.address.postcode,
            "country": self.address.country,
        }

    def test_address_serialization(self):
        serializer = AddressSerializer(instance=self.address)
        self.assertEqual(serializer.data, self.address_data)

    def test_address_deserialization(self):
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(Address.objects.count(), 1)


class CompanySerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.address = AddressFactory.create()
        self.company = CompanyFactory.build(address=self.address)
        self.company_data = {
            "id": self.company.id,
            "name": self.company.name,
            "krs": self.company.krs,
            "regon": self.company.regon,
            "nip": self.company.nip,
            "address": self.company.address.id,
            "is_mine": self.company.is_mine,
            "shortcut": str(self.company.shortcut),
        }

    def test_company_serialization(self):
        serializer = CompanySerializer(instance=self.company)
        self.assertEqual(serializer.data, self.company_data)

    def test_company_deserialization(self):
        serializer = CompanySerializer(data=self.company_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Company.objects.count(), 1)


class ContactSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory.create()
        self.contact = ContactFactory.build(company=self.company)
        self.contact_data = {
            "id": self.contact.id,
            "name": self.contact.name,
            "email": self.contact.email,
            "phone": self.contact.phone,
            "description": self.contact.description,
            "company": self.contact.company.id,
        }

    def test_contact_serialization(self):
        serializer = ContactSerializer(instance=self.contact)
        self.assertEqual(serializer.data, self.contact_data)

    def test_contact_deserialization(self):
        serializer = ContactSerializer(data=self.contact_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Contact.objects.count(), 1)
