from http import HTTPStatus

from common_tests.EDMSTestCase import EDMSTestCase
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from users.factories import UserFactory

User = get_user_model()


class TestCaseCustomLoginView(EDMSTestCase):
    def setUp(self):
        super().setUp()
        # self.user = UserFactory.create(password=self.password)
        self.not_active_user = UserFactory.create(password=self.password, is_active=False)
        self.not_existed_user = UserFactory.build(password=self.password)

    def test_render_if_user_not_logged_in(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/login.html")

    def test_redirect_if_user_is_logged_in(self):
        login = self.client.login(email=self.ceo.email, password=self.password)
        self.assertTrue(login)

        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("dashboard"))

    def test_unsuccessfully_login_unactivated_user(self):
        form_data = {"username": self.not_active_user.email, "password": self.password}
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(
            message,
            "Invalid email or password.",
        )

    def test_successfully_login_activated_user(self):
        form_data = {"username": self.ceo.email, "password": self.password}
        self.ceo.save()
        response = self.client.post(reverse("login"), data=form_data)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(self.ceo.is_authenticated)

    def test_unsuccessfully_login_if_wrong_password(self):
        form_data = {"username": self.ceo.email, "password": "whatever"}
        self.ceo.save()
        self.assertTrue(User.objects.get(email=self.ceo.email).is_active)
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/login.html")
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Invalid email or password.")

    def test_unsuccessfully_login_because_user_does_not_exist(self):
        form_data = {
            "username": self.not_existed_user.email,
            "password": self.password,
        }
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/login.html")

        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(message, "Invalid email or password.")


class TestCaseCustomLogoutView(TestCase):
    def setUp(self):
        self.password = User.objects.make_random_password()
        self.user = UserFactory.create(password=self.password)

    def test_logout_user_successfully(self):
        login = self.client.login(email=self.user.email, password=self.password)
        self.assertTrue(login)
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.post(reverse("logout"))
        self.assertFalse("_auth_user_id" in self.client.session)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login_logout/logout.html")
