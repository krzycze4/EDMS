from django.test import TestCase
from employees.factories.factories_agreement import AgreementFactory
from users.factories import UserFactory
from users.tasks import set_user_is_active_to_false


class SetUserIsActiveToFalseTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=False)
        self.superuser = UserFactory(is_superuser=True)

    def test_user_is_deactivated_if_no_current_agreement(self):
        set_user_is_active_to_false()
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_user_is_not_deactivated_if_current_agreement_exists(self):
        AgreementFactory.create(user=self.user)
        set_user_is_active_to_false()
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_superuser_is_not_deactivated(self):
        set_user_is_active_to_false()
        self.superuser.refresh_from_db()
        self.assertTrue(self.superuser.is_active)
