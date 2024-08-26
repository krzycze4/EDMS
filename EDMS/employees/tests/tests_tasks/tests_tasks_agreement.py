from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.tasks.tasks_agreement import set_agreement_is_current


class AgreementTasksTests(TestCase):
    def setUp(self) -> None:
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        one_year_ahead = today + timezone.timedelta(days=365)
        one_year_back = today - timezone.timedelta(days=366)
        self.agreement_starting_today = AgreementFactory.create(
            create_date=today, start_date=today, end_date=one_year_ahead, end_date_actual=one_year_ahead
        )
        self.agreement_ending_yesterday = AgreementFactory.create(
            create_date=one_year_back, start_date=one_year_back, end_date=yesterday, end_date_actual=yesterday
        )

    def test_set_agreement_is_current_for_starting_agreement(self):
        set_agreement_is_current()
        self.agreement_starting_today.refresh_from_db()
        self.assertTrue(self.agreement_starting_today.is_current)

    def test_set_agreement_is_current_for_ending_agreement(self):
        set_agreement_is_current()
        self.agreement_ending_yesterday.refresh_from_db()
        self.assertFalse(self.agreement_ending_yesterday.is_current)
