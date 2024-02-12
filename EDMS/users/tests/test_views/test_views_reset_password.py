from http import HTTPStatus

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.models import User


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
        self.assertTemplateUsed(response, "users/forgot_password/forgot_password.html")

    def test_redirect_if_form_is_valid(self):
        email = "email@email.com"
        response = self.client.post(reverse("forgot-password"), data={"email": email})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("forgot-password-done"))


class TestCaseCustomPasswordResetDoneView(TestCase):
    def test_status_and_template(self):
        response = self.client.get(reverse("forgot-password-done"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response, "users/forgot_password/forgot_password_done.html"
        )


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
        self.assertTemplateUsed(
            response, "users/forgot_password/forgot_password_confirm.html"
        )
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
        self.assertTemplateUsed(
            response, "users/forgot_password/forgot_password_complete.html"
        )
