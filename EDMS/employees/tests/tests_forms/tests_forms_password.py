from django.test import TestCase
from django.utils.crypto import get_random_string
from employees.forms.forms_password import CustomPasswordChangeForm
from users.factories import UserFactory


class CustomPasswordChangeFormTests(TestCase):
    def setUp(self) -> None:
        old_password = get_random_string(length=12)
        new_password = get_random_string(length=12)
        self.form_data = {
            "old_password": old_password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        self.user = UserFactory.create(password=old_password)

    def test_form_valid(self):
        form = CustomPasswordChangeForm(data=self.form_data, user=self.user)
        self.assertTrue(form.is_valid())
