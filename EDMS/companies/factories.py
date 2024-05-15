import factory
from companies.models import Address, Company, Contact
from factory.django import DjangoModelFactory


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
    krs = factory.Faker("pyint", min_value=10000000000000, max_value=99999999999999)
    regon = factory.Faker("pyint", min_value=100000000, max_value=999999999)
    nip = factory.Faker("pyint", min_value=1000000000, max_value=9999999999)
    address = factory.SubFactory(AddressFactory)
    is_mine = True
    shortcut = factory.LazyAttribute(lambda company: company.name[:4])


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact

    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    description = factory.Faker("sentence")
    company = factory.SubFactory(CompanyFactory)
