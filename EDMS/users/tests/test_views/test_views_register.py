from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django import forms
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, tag
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.factories import UserFactory
from users.forms.forms_custom_user_creation import CustomUserCreationForm
from users.tokens import account_activation_token

User = get_user_model()


class TestCaseUserRegisterView(EDMSTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.stub_user = UserFactory.stub(password=cls.password)
        cls.valid_form = {
            "first_name": cls.stub_user.first_name,
            "last_name": cls.stub_user.last_name,
            "email": cls.stub_user.email,
            "password1": cls.password,
            "password2": cls.password,
        }
        cls.invalid_form_different_passwords = {
            "first_name": cls.stub_user.first_name,
            "last_name": cls.stub_user.last_name,
            "email": cls.stub_user.email,
            "password1": cls.password,
            "password2": "whatever",
        }
        cls.invalid_form_existing_user = {
            "first_name": cls.ceo.first_name,
            "last_name": cls.ceo.last_name,
            "email": cls.ceo.email,
            "password1": cls.password,
            "password2": cls.password,
        }

    def test_redirect_to_dashboard_for_authenticated_user(self):
        login = self.client.login(username=self.ceo.email, password=self.password)
        self.assertTrue(login)

        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("dashboard"))

    def test_access_for_unauthenticated_user(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/register.html")

    def test_display_form(self):
        response = self.client.get(reverse("register"))
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    @tag("celery")
    def test_register_user_successfully(self):
        response = self.client.post(reverse("register"), data=self.valid_form)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("success-register"))
        self.assertTrue(User.objects.filter(email=self.valid_form["email"]).exists())

    @tag("celery")
    def test_sending_email_with_token_and_uidb64_if_successfully_registration(self):
        response = self.client.post(reverse("register"), data=self.valid_form)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(response, "email_templates/account_activation_email.html")

        token = response.context["token"]
        self.assertEqual(len(token), 39)

        self.assertEqual(User.objects.count(), 2)
        uidb64 = response.context["uidb64"]
        self.assertEqual(int(urlsafe_base64_decode(uidb64)), User.objects.last().pk)

    def test_not_create_user_if_form_is_invalid(self):
        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 4)

        response = self.client.post(reverse("register"), data=self.invalid_form_different_passwords)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/register.html")

        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 4)

    def test_not_create_user_if_user_exists_in_database(self):
        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 4)

        response = self.client.post(reverse("register"), data=self.invalid_form_existing_user)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/register.html")
        self.assertRaises(forms.ValidationError)


class TestCaseSuccessRegisterView(TestCase):
    def test_render_page(self):
        response = self.client.get(reverse("success-register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/register_success.html")


class TestCaseActivateAccountView(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=False)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_user_successfully(self):
        self.assertFalse(self.user.is_active)
        response = self.client.get(reverse("activate-account", kwargs={"uidb64": self.uidb64, "token": self.token}))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "successfully")
        self.assertTrue(self.user.is_active)

    def test_user_activation_failure_uidb64(self):
        response = self.client.get(reverse("activate-account", kwargs={"uidb64": "invalid", "token": self.token}))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "failed")
        self.assertFalse(self.user.is_active)

    def test_user_activation_failure_token(self):
        response = self.client.get(reverse("activate-account", kwargs={"uidb64": self.uidb64, "token": "invalid"}))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "failed")
        self.assertFalse(self.user.is_active)

    def test_user_activation_when_user_does_not_exist(self):
        uidb64_not_existing_user = urlsafe_base64_encode(force_bytes(2))
        response = self.client.get(
            reverse(
                "activate-account",
                kwargs={"uidb64": uidb64_not_existing_user, "token": self.token},
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "failed")
        self.assertFalse(self.user.is_active)
