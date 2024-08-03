import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory import post_generation
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    phone_number = factory.Faker("phone_number")
    position = "position"
    vacation_days_per_year = 26
    vacation_left = 0
    address = None

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.password = make_password(extracted)
        else:
            self.password = make_password("default_password")
