from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from users.models import User


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
        self.assertTemplateUsed(response, "users/login_logout/login.html")

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
        self.assertTemplateUsed(response, "users/login_logout/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(
            message,
            "Invalid email or password.",
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
        self.assertTemplateUsed(response, "users/login_logout/login.html")
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Invalid email or password.")

    def test_unsuccessfully_login_because_user_does_not_exist(self):
        form_data = {
            "username": "email_does_not_exist@email.com",
            "password": "edmsedms2",
        }
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Invalid email or password.")


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
        self.assertTemplateUsed(response, "users/login_logout/logout.html")
