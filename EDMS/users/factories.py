import io

import factory
from companies.factories import AddressFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from factory import post_generation
from factory.django import DjangoModelFactory
from PIL import Image

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = False
    phone_number = factory.Faker("phone_number")
    position = "position"
    vacation_days_per_year = 26
    vacation_left = 0
    address = factory.SubFactory(AddressFactory)

    @factory.lazy_attribute
    def photo(self):
        image = Image.new("RGB", (100, 100), color="red")
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return ContentFile(buffer.getvalue(), "test_image.png")

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.password = make_password(extracted)
        else:
            self.password = make_password("default_password")
