from django.contrib.auth import get_user_model
from django.test import TestCase
from users.factories import UserFactory
from users.forms.forms_custom_user_creation import CustomUserCreationForm

User = get_user_model()


class TestCaseCustomUserCreationForm(TestCase):
    def setUp(self):
        self.password = User.objects.make_random_password()
        self.build_user = UserFactory.build(password=self.password)
        self.create_user = UserFactory.create(password=self.password)
        self.not_saved_user = UserFactory.build(password=self.password)
        self.valid_form = CustomUserCreationForm(
            data={
                "first_name": self.build_user.first_name,
                "last_name": self.build_user.last_name,
                "email": self.build_user.email,
                "password1": self.password,
                "password2": self.password,
            }
        )
        self.invalid_form = CustomUserCreationForm(
            data={
                "first_name": self.not_saved_user.first_name,
                "last_name": self.not_saved_user.last_name,
                "email": self.create_user.email,
                "password1": self.password,
                "password2": self.password,
            }
        )

    def test_form_valid(self):
        self.assertTrue(self.valid_form.is_valid())

    def test_form_invalid_because_email_in_form_exists_in_database(self):
        self.assertEqual(
            self.invalid_form.errors["email"], [f"Email '{self.create_user.email}' has been already used."]
        )
        self.assertFalse(self.invalid_form.is_valid())
