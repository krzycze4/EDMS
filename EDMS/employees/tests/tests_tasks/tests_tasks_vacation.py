from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_vacation import VacationFactory
from employees.tasks.tasks_vacation import (
    count_granted_vacation_from_agreement,
    count_work_months_current_year,
    set_user_vacation_left,
)
from users.factories import UserFactory


class VacationTasksTest(TestCase):
    def setUp(self):
        today = timezone.now().date()
        month_back = today - timezone.timedelta(days=30)
        ahead_date = today + timezone.timedelta(days=300)
        one_week_ahead = today + timezone.timedelta(days=7)
        two_week_ahead = today + timezone.timedelta(days=14)

        self.user = UserFactory.create(vacation_days_per_year=20)
        self.agreement = AgreementFactory.create(
            create_date=today, start_date=month_back, end_date=ahead_date, end_date_actual=ahead_date, user=self.user
        )
        self.vacation = VacationFactory.create(
            start_date=one_week_ahead, end_date=two_week_ahead, leave_user=self.user, included_days_off=2
        )

    def test_set_user_vacation_left(self):
        initial_vacation_left = self.user.vacation_left
        set_user_vacation_left()
        self.user.refresh_from_db()
        self.assertGreater(self.user.vacation_left, initial_vacation_left)

    def test_count_granted_vacation(self):
        granted_vacation = count_granted_vacation_from_agreement(
            current_employment_agreement=self.agreement, user=self.user
        )
        self.assertGreater(granted_vacation, 0)

    def test_count_work_months_partial_year(self):
        start_date = timezone.datetime(2024, 5, 1).date()
        end_date_actual = timezone.datetime(2024, 12, 31).date()
        work_months = count_work_months_current_year(start_date=start_date, end_date_actual=end_date_actual)
        self.assertEqual(work_months, 8)

    def test_count_work_months_full_year(self):
        start_date = timezone.datetime(2024, 1, 1).date()
        end_date_actual = timezone.datetime(2024, 12, 31).date()
        work_months = count_work_months_current_year(start_date=start_date, end_date_actual=end_date_actual)
        self.assertEqual(work_months, 12)

    def test_start_date_in_previous_year(self):
        current_year = timezone.now().year
        start_date = timezone.datetime(current_year - 1, 11, 1)
        end_date_actual = timezone.datetime(current_year, 5, 31)
        result = count_work_months_current_year(start_date, end_date_actual)
        self.assertEqual(result, 5)
