from django.test import TestCase
from users.forms.forms_custom_user_creation import CustomUserCreationForm
from users.models import User


class TestCaseCustomUserCreationForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsemds1",
        )

    def test_form_valid(self):
        form = CustomUserCreationForm(
            data={
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email1@email.com",
                "password1": "edmsedms1",
                "password2": "edmsedms1",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_because_email_in_form_exists_in_database(self):
        form = CustomUserCreationForm(
            data={
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email@email.com",
                "password1": "edmsedms1",
                "password2": "edmsedms1",
            }
        )
        self.assertEqual(form.errors["email"], ["Email 'email@email.com' has been already used."])
        self.assertFalse(form.is_valid())
