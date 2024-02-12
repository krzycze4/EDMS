from http import HTTPStatus

from django import forms
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.forms.forms_custom_user_creation import CustomUserCreationForm
from users.models import User
from users.tokens import account_activation_token


class TestCaseUserRegisterView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "edmsemds1"
        cls.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password=cls.password,
        )

    def test_redirect_to_dashboard_for_authenticated_user(self):
        login = self.client.login(username=self.user.email, password=self.password)
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

    def test_register_user_successfully(self):
        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "email2@email.com",
            "password1": "edmsedms1",
            "password2": "edmsedms1",
        }

        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("success-register"))
        self.assertTrue(User.objects.filter(email=form_data["email"]).exists())

    def test_sending_email_with_token_and_uidb64_if_successfully_registration(self):
        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "email2@email.com",
            "password1": "edmsedms1",
            "password2": "edmsedms1",
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(response, "emails/account_activation_email.html")

        token = response.context["token"]
        self.assertEqual(len(token), 39)

        self.assertEqual(User.objects.count(), 2)
        uidb64 = response.context["uidb64"]
        self.assertEqual(int(urlsafe_base64_decode(uidb64)), User.objects.last().pk)

    def test_not_create_user_if_form_is_invalid(self):
        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 1)

        invalid_form_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "email2@email.com",
            "password1": "edmsedms1",
            "password2": "edmsedms2",
        }

        response = self.client.post(reverse("register"), data=invalid_form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/register.html")

        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 1)

    def test_not_create_user_if_user_exists_in_database(self):
        number_users_in_database = User.objects.count()
        self.assertEqual(number_users_in_database, 1)

        form_data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "email@email.com",
            "password1": "edmsedms1",
            "password2": "edmsedms1",
        }

        response = self.client.post(reverse("register"), data=form_data)
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
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsedms1",
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_user_successfully(self):
        self.assertFalse(self.user.is_active)
        response = self.client.get(
            reverse(
                "activate-account", kwargs={"uidb64": self.uidb64, "token": self.token}
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "successfully")
        self.assertTrue(self.user.is_active)

    def test_user_activation_failure_uidb64(self):
        response = self.client.get(
            reverse(
                "activate-account", kwargs={"uidb64": "invalid", "token": self.token}
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register/activation_result.html")
        self.assertEqual(response.context["information"], "failed")
        self.assertFalse(self.user.is_active)

    def test_user_activation_failure_token(self):
        response = self.client.get(
            reverse(
                "activate-account", kwargs={"uidb64": self.uidb64, "token": "invalid"}
            )
        )
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
