from companies.factories import AddressFactory
from django.test import TestCase
from employees.forms.forms_address import AddressForm


class AddressFormTests(TestCase):
    def setUp(self) -> None:
        self.address = AddressFactory.build()

    def test_if_form_is_valid(self):
        form = AddressForm(
            data={
                "street_name": self.address.street_name,
                "street_number": self.address.street_number,
                "city": self.address.city,
                "postcode": self.address.postcode,
                "country": self.address.country,
            }
        )
        self.assertTrue(form.is_valid())
