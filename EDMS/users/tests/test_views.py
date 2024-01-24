from http import HTTPStatus

from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.forms import CustomUserCreationForm
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
        self.assertTemplateUsed(response, "users/register.html")

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
        self.assertTemplateUsed(response, "users/register.html")

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
        self.assertTemplateUsed(response, "users/register.html")
        self.assertRaises(forms.ValidationError)


class TestCaseSuccessRegisterView(TestCase):
    def test_render_page(self):
        response = self.client.get(reverse("success-register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/register_success.html")


class TestCaseCustomLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsedms1",
        )

    def test_render_if_user_not_logged_in(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

    def test_redirect_if_user_is_logged_in(self):
        login = self.client.login(email="email@email.com", password="edmsedms1")
        self.assertTrue(login)

        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("dashboard"))

    def test_unsuccessfully_login_unactivated_user(self):
        form_data = {"username": "email@email.com", "password": "edmsedms1"}
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(
            message,
            "User is not active. Please check your email and active your account.",
        )

    def test_successfully_login_activated_user(self):
        form_data = {"username": "email@email.com", "password": "edmsedms1"}
        self.user.is_active = True
        self.user.save()
        response = self.client.post(reverse("login"), data=form_data)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(self.user.is_authenticated)

    def test_unsuccessfully_login_if_wrong_password(self):
        form_data = {"username": "email@email.com", "password": "edmsedms2"}
        self.user.is_active = True
        self.user.save()
        self.assertTrue(User.objects.get(email=self.user.email).is_active)
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Incorrect password!")

    def test_unsuccessfully_login_because_user_does_not_exist(self):
        form_data = {
            "username": "email_does_not_exist@email.com",
            "password": "edmsedms2",
        }
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(
            message, "User does not exist. Please check your email and password."
        )


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
        self.assertTemplateUsed(response, "users/activation_result.html")
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
        self.assertTemplateUsed(response, "users/activation_result.html")
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
        self.assertTemplateUsed(response, "users/activation_result.html")
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
        self.assertTemplateUsed(response, "users/activation_result.html")
        self.assertEqual(response.context["information"], "failed")
        self.assertFalse(self.user.is_active)


class TestCaseCustomPasswordResetView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsedms1",
        )

    def test_render_page(self):
        response = self.client.get(reverse("forgot-password"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/forgot_password.html")

    def test_redirect_if_form_is_valid(self):
        email = "email@email.com"
        response = self.client.post(reverse("forgot-password"), data={"email": email})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("forgot-password-done"))


class TestCaseCustomPasswordResetDoneView(TestCase):
    def test_status_and_template(self):
        response = self.client.get(reverse("forgot-password-done"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/forgot_password_done.html")


class TestCaseCustomPasswordResetConfirmView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsedms1",
            is_active=True,
        )
        token_generator = PasswordResetTokenGenerator()
        self.token = token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

    def test_redirect_to_set_password_page(self):
        response = self.client.get(
            reverse(
                "forgot-password-confirm",
                kwargs={"uidb64": self.uidb64, "token": self.token},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, f"/forgot-password/{self.uidb64}/set-password/")

    def test_render_set_password_page(self):
        response = self.client.get(f"/forgot-password/{self.uidb64}/set-password/")
        self.assertTemplateUsed(response, "users/forgot_password_confirm.html")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_change_password_with_different_new_passwords(self):
        form_data = {"new_password1": "Edmsedms2", "new_password2": "edmsedms2"}

        password_before = self.user.password

        response = self.client.get(
            reverse(
                "forgot-password-confirm",
                kwargs={"uidb64": self.uidb64, "token": self.token},
            )
        )
        redirected_url = response.url

        response = self.client.post(redirected_url, data=form_data)

        self.user.refresh_from_db()
        password_after = self.user.password

        self.assertEqual(password_after, password_before)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.request["PATH_INFO"], redirected_url)

    def test_change_password_correctly(self):
        form_data = {"new_password1": "Edmsedms2", "new_password2": "Edmsedms2"}

        password_before = self.user.password

        response = self.client.get(
            reverse(
                "forgot-password-confirm",
                kwargs={"uidb64": self.uidb64, "token": self.token},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        redirected_url = response.url

        response = self.client.post(redirected_url, data=form_data)

        self.user.refresh_from_db()
        password_after = self.user.password

        self.assertNotEqual(password_after, password_before)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("forgot-password-complete"))


class TestCaseCustomPasswordResetCompleteView(TestCase):
    def test_render_forgot_password_complete(self):
        response = self.client.get(reverse("forgot-password-complete"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/forgot_password_complete.html")


class TestCaseCustomLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="First",
            last_name="Last",
            email="email@email.com",
            password="edmsedms1",
            is_active=True,
        )

    def test_logout_user_successfully(self):
        login = self.client.login(email="email@email.com", password="edmsedms1")
        self.assertTrue(login)
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.post(reverse("logout"))
        self.assertFalse("_auth_user_id" in self.client.session)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/logout.html")
