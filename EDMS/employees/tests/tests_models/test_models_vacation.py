from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_vacation import VacationFactory
from employees.models.models_agreement import Agreement
from employees.models.models_vacation import Vacation
from users.factories import UserFactory


class ModelVacationTests(TestCase):
    def setUp(self) -> None:
        self.leave_user = UserFactory.create()
        self.substitute_users = UserFactory.create_batch(2)
        self.vacation = VacationFactory.build(leave_user=self.leave_user, substitute_users=self.substitute_users)
        self.employment_agreement = AgreementFactory.build(
            start_date=timezone.datetime(timezone.now().year, 1, 1).date(),
            end_date=timezone.datetime(timezone.now().year, 12, 31).date(),
            user=self.leave_user,
        )

    def test_save_vacation(self):
        count_vacations_before_save = Vacation.objects.count()
        self.assertEqual(count_vacations_before_save, 0)
        self.vacation.save()
        self.assertEqual(count_vacations_before_save + 1, Vacation.objects.count())

    def test_delete_vacation(self):
        self.vacation.save()
        count_vacations_before_delete = Vacation.objects.count()
        self.assertEqual(count_vacations_before_delete, 1)
        self.vacation.delete()
        self.assertEqual(count_vacations_before_delete - 1, Vacation.objects.count())

    def test_count_leave_user_vacation_left_when_agreement_type_is_employment(self):
        self.assertEqual(self.leave_user.vacation_left, 0)
        self.employment_agreement.save()
        self.assertEqual(self.leave_user.vacation_left, self.leave_user.vacation_days_per_year)

    def test_count_leave_user_vacation_left_when_agreement_type_is_not_employment(self):
        self.assertEqual(self.leave_user.vacation_left, 0)
        AgreementFactory.create(type=Agreement.COMMISSION, user=self.leave_user)
        self.assertEqual(self.leave_user.vacation_left, 0)

    def test_count_leave_user_vacation_left_when_agreement_delete(self):
        self.assertEqual(self.leave_user.vacation_left, 0)
        self.employment_agreement.save()
        self.assertEqual(self.leave_user.vacation_left, 26)
        self.employment_agreement.delete()
        self.assertEqual(self.leave_user.vacation_left, 0)

    def test_count_used_vacation_when_vacation_type_is_annual(self):
        self.vacation.save()
        expected_used_vacation = (
            (self.vacation.end_date - self.vacation.start_date).days - self.vacation.included_days_off + 1
        )
        self.assertEqual(self.vacation.count_used_vacation(), expected_used_vacation)
