from companies.factories import AddressFactory, CompanyFactory
from companies.forms.forms_company_and_address import (
    CompanyAndAddressForm,
    KRSForm,
    UpdateAddressForm,
    UpdateCompanyIdentifiersForm,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestCaseKRSForm(TestCase):
    def test_form_valid(self):
        form = KRSForm(data={"krs_id": 10**13})  # 14 digits
        self.assertTrue(form.is_valid())

    def test_form_invalid_too_long_number(self):
        form = KRSForm(data={"krs_id": 10**14})  # 15 digits
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)


class TestCaseCompanyAndAddressForm(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory(is_mine=False)

    def test_form_valid(self):
        form = CompanyAndAddressForm(
            data={
                "name": self.company.name,
                "krs": self.company.krs,
                "regon": self.company.regon,
                "nip": self.company.nip,
                "street_name": self.company.address.street_name,
                "street_number": self.company.address.street_number,
                "city": self.company.address.city,
                "postcode": self.company.address.postcode,
                "country": self.company.address.country,
                "shortcut": self.company.shortcut,
                "is_mine": self.company.is_mine,
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_mine_field_exists_if_my_company_not_in_db(self):
        form = CompanyAndAddressForm()
        self.assertTrue("is_mine" in form.fields)

    def test_is_mine_field_exists_if_my_company_in_db(self):
        self.my_company = CompanyFactory()
        form = CompanyAndAddressForm()
        self.assertFalse("is_mine" in form.fields)


class TestCaseUpdateCompanyIdentifiersForm(TestCase):
    def setUp(self) -> None:
        self.company1 = CompanyFactory()
        self.company2 = CompanyFactory()

    def test_form_valid(self):
        form = UpdateCompanyIdentifiersForm(
            instance=self.company1,
            data={
                "name": self.company1.name,
                "krs": self.company1.krs,
                "regon": self.company1.regon,
                "nip": self.company1.nip,
                "shortcut": self.company1.shortcut,
                "is_mine": self.company1.is_mine,
            },
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_existing_shortcut(self):
        form = UpdateCompanyIdentifiersForm(
            instance=self.company1,
            data={
                "name": self.company1.name,
                "krs": self.company1.krs,
                "regon": self.company1.regon,
                "nip": self.company1.nip,
                "shortcut": self.company2.shortcut,
                "is_mine": self.company1.is_mine,
            },
        )
        self.assertFalse(form.is_valid())


class TestCaseUpdateAddressForm(TestCase):
    def setUp(self) -> None:
        self.address = AddressFactory()

    def test_form_valid(self):
        form = UpdateAddressForm(
            instance=self.address,
            data={
                "street_name": self.address.street_name,
                "street_number": self.address.street_number,
                "city": self.address.city,
                "postcode": self.address.postcode,
                "country": self.address.country,
            },
        )
        self.assertTrue(form.is_valid())
