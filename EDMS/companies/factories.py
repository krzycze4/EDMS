import factory
from companies.models import Address, Company, Contact
from factory import Sequence
from factory.django import DjangoModelFactory

used_numbers = set()


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    street_name = factory.Faker("street_name")
    street_number = factory.Faker("pyint", min_value=0, max_value=100)
    city = factory.Faker("city")
    postcode = factory.Faker("postcode")
    country = factory.Faker("country")


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    krs = Sequence(lambda n: 10000000000000 + n)
    regon = Sequence(lambda n: 100000000 + n)
    nip = Sequence(lambda n: 1000000000 + n)
    address = factory.SubFactory(AddressFactory)
    is_mine = False
    shortcut = factory.Faker("bothify", text="??###")


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    description = factory.Faker("sentence")
    company = factory.SubFactory(CompanyFactory)
