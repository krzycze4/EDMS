import unicodedata

from django.test import TestCase
from users.models import User


class TestCaseCustomUserManager(TestCase):
    def setUp(self):
        self.email = "email@email.com"
        self.password = "edmsedms1"

    def test_create_user(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.email, password=self.password
        )
        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_superuser_failure_is_staff_false(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email=self.email, password=self.password, is_staff=False
            )

        self.assertEqual(str(context.exception), "Superuser must have is_staff=True.")

    def test_create_superuser_failure_is_superuser_false(self):
        with self.assertRaises(ValueError) as context:
            User.objects.create_superuser(
                email=self.email, password=self.password, is_superuser=False
            )
        self.assertTrue(
            str(context.exception), "Superuser must have is_superuser=True."
        )

    def test_get_by_natural_key(self):
        self.user = User.objects.create_user(email=self.email, password=self.password)
        user_get_by_natural_key = User.objects.get_by_natural_key(email=self.email)
        self.assertTrue(user_get_by_natural_key, self.user)


class TestCaseUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="email@email.com", password="edmsedms1"
        )

    def test_get_username(self):
        user_email = User.get_username(self.user)
        self.assertEqual(user_email, self.user.email)

    def test_normalize_username_without_accented_character(self):
        email = self.user.email
        normalized_email = User.normalize_email(email)
        self.assertEqual(normalized_email, self.user.email)

    def test_normalize_username_with_accented_character(self):
        email = "\u2161@email.com"
        normalized_email = User.normalize_username(email)
        expected_normalized_email = unicodedata.normalize("NFKC", email)
        self.assertEqual(normalized_email, expected_normalized_email)

    def test_normalize_email_without_accented_character(self):
        email = self.user.email
        normalized_email = User.normalize_email(email)
        self.assertTrue(normalized_email, email)

    def test_normalize_email_with_accented_character(self):
        email = "\u2161@email.com"
        normalized_email = User.normalize_email(email)
        expected_normalize_email = unicodedata.normalize("NFKC", email)
        self.assertTrue(normalized_email, expected_normalize_email)

    def test_str(self):
        self.assertEqual(self.user.email, str(self.user))
