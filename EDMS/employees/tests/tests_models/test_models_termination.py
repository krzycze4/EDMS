from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_termination import Termination


class ModelTerminationTests(TestCase):
    def setUp(self) -> None:
        self.agreement = AgreementFactory.create()
        self.termination = TerminationFactory.build(agreement=self.agreement)

    def test_return_string(self):
        self.assertEqual(str(self.termination), f"Termination #{self.termination.name}")

    def test_update_agreement_end_date_actual_to_termination_end_date_when_create_termination(self):
        self.assertEqual(self.agreement.end_date_actual, self.agreement.end_date)
        self.termination.save()
        self.assertEqual(self.agreement.end_date_actual, self.termination.end_date)

    def test_update_agreement_end_date_actual_to_addendum_end_date_when_addendum_exists_delete_termination(self):
        self.assertEqual(self.agreement.end_date_actual, self.agreement.end_date)
        addendum = AddendumFactory.create(agreement=self.agreement)
        self.assertEqual(self.agreement.end_date_actual, addendum.end_date)
        self.termination.save()
        self.assertEqual(self.agreement.end_date_actual, self.termination.end_date)
        self.termination.delete()
        self.assertEqual(self.agreement.end_date_actual, addendum.end_date)

    def test_update_agreement_end_date_actual_to_agreement_end_date_if_addendum_not_exist_and_delete_termination(self):
        self.assertEqual(self.agreement.end_date_actual, self.agreement.end_date)
        self.termination.save()
        self.assertEqual(self.agreement.end_date_actual, self.termination.end_date)
        self.termination.delete()
        self.assertEqual(self.agreement.end_date_actual, self.agreement.end_date)

    def test_set_agreement_is_current_as_true_when_agreement_end_date_actual_is_in_future(self):
        self.assertTrue(self.agreement.is_current)

    def test_set_agreement_is_current_as_true_when_agreement_end_date_actual_is_in_past(self):
        self.agreement.end_date = timezone.now().date() - timezone.timedelta(days=1)
        self.agreement.end_date_actual = self.agreement.end_date
        self.agreement.save()
        self.assertFalse(self.agreement.is_current)

    def test_save_termination(self):
        count_terminations_before_save = Termination.objects.count()
        self.assertEqual(count_terminations_before_save, 0)
        self.termination.save()
        self.assertEqual(count_terminations_before_save + 1, Termination.objects.count())

    def test_delete_termination(self):
        self.termination.save()
        count_terminations_before_delete = Termination.objects.count()
        self.assertEqual(count_terminations_before_delete, 1)
        self.termination.delete()
        self.assertEqual(count_terminations_before_delete - 1, Termination.objects.count())
