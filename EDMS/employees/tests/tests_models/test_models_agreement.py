from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_agreement import Agreement
from users.factories import UserFactory


class ModelAgreementTests(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.agreement = AgreementFactory.build(user=self.user)

    def test_return_str(self):
        self.assertEqual(str(self.agreement), f"{self.agreement.name}")

    def test_save_agreement_to_db(self):
        count_agreement_before_save = Agreement.objects.count()
        self.agreement.save()
        self.assertEqual(Agreement.objects.count(), count_agreement_before_save + 1)

    def test_delete_agreement_from_db(self):
        self.agreement.save()
        count_agreement_before_delete = Agreement.objects.count()
        self.agreement.delete()
        self.assertEqual(Agreement.objects.count(), count_agreement_before_delete - 1)

    def test_set_agreement_end_date_actual_as_agreement_end_date_when_agreement_created(self):
        self.agreement.save()
        self.assertEqual(self.agreement.end_date, self.agreement.end_date_actual)

    def test_set_agreement_end_date_actual_as_agreement_end_date_when_update_agreement_without_addendum(self):
        self.agreement.save()
        self.agreement.salary_gross = Decimal(10)
        self.agreement.save()
        self.assertEqual(self.agreement.end_date, self.agreement.end_date_actual)

    def test_set_is_current_true_when_today_date_is_between_agreement_start_date_and_agreement_end_date(self):
        self.agreement.save()
        self.assertTrue(self.agreement.is_current)

    def test_set_is_current_false_when_today_date_is_after_agreement_end_date(self):
        self.agreement.create_date = timezone.now().date() - timezone.timedelta(days=2)
        self.agreement.start_date = timezone.now().date() - timezone.timedelta(days=2)
        self.agreement.end_date = timezone.now().date() - timezone.timedelta(days=1)
        self.agreement.save()
        self.assertFalse(self.agreement.is_current)

    def test_set_is_current_false_when_today_date_is_before_agreement_start_date(self):
        self.agreement.start_date = timezone.now().date() + timezone.timedelta(days=1)
        self.agreement.end_date = timezone.now().date() + timezone.timedelta(days=2)
        self.agreement.save()
        self.assertFalse(self.agreement.is_current)

    def test_count_user_vacation_left_when_create_employment_agreement(self):
        self.agreement.start_date = timezone.datetime(timezone.now().year, 1, 1).date()
        self.agreement.end_date = timezone.datetime(timezone.now().year, 12, 31).date()
        self.assertEqual(self.user.vacation_left, 0)
        self.agreement.save()
        self.assertEqual(self.user.vacation_left, self.user.vacation_days_per_year)

    def test_count_user_vacation_left_when_create_agreement_different_than_employment_agreement(self):
        self.agreement.start_date = timezone.datetime(timezone.now().year, 1, 1).date()
        self.agreement.end_date = timezone.datetime(timezone.now().year, 12, 31).date()
        self.assertEqual(self.user.vacation_left, 0)
        self.agreement.type = Agreement.COMMISSION
        self.agreement.save()
        self.assertEqual(self.user.vacation_left, 0)

    def test_count_work_month(self):
        self.agreement.start_date = timezone.datetime(timezone.now().year, 7, 1).date()
        self.agreement.end_date = timezone.datetime(timezone.now().year, 12, 31).date()
        self.agreement.save()
        expected_vacation_left = self.agreement.end_date.month - self.agreement.start_date.month + 1
        self.assertEqual(self.agreement.count_work_months_current_year(), expected_vacation_left)
