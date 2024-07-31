from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_addendum import Addendum


class ModelAddendumTests(TestCase):
    def setUp(self) -> None:
        self.current_agreement = AgreementFactory.create(create_date=timezone.now().date() - timezone.timedelta(days=2))

        self.not_current_agreement = AgreementFactory.create(
            create_date=timezone.now().date() - timezone.timedelta(days=10),
            start_date=timezone.now().date() - timezone.timedelta(days=10),
            end_date=timezone.now().date() - timezone.timedelta(days=5),
        )

        self.addendum_current = AddendumFactory.build(
            create_date=timezone.now().date() - timezone.timedelta(days=2),
            end_date=timezone.now().date() + timezone.timedelta(days=20),
            agreement=self.current_agreement,
        )

        self.addendum_not_current = AddendumFactory.build(
            end_date=timezone.now().date() + timezone.timedelta(days=20), agreement=self.not_current_agreement
        )

        self.second_addendum = AddendumFactory.build(
            end_date=timezone.now().date() + timezone.timedelta(days=30), agreement=self.current_agreement
        )

    def test_verbose_name_plural(self):
        self.assertEqual(Addendum._meta.verbose_name_plural, "Addenda")

    def test_return_str(self):
        self.assertEqual(str(self.addendum_current), f"Addendum #{self.addendum_current.name}")

    def test_update_agreement_end_date_actual_when_addendum_save(self):
        self.addendum_current.save()
        self.assertEqual(self.current_agreement.end_date_actual, self.addendum_current.end_date)

    def test_update_agreement_end_date_actual_when_addendum_delete(self):
        self.addendum_current.save()
        self.assertEqual(self.current_agreement.end_date_actual, self.addendum_current.end_date)
        self.addendum_current.delete()
        self.assertEqual(self.current_agreement.end_date_actual, self.current_agreement.end_date)

    def test_set_agreement_is_current_as_true_when_addendum_delete(self):
        self.addendum_current.save()
        self.assertEqual(self.current_agreement.is_current, True)
        self.addendum_current.delete()
        self.assertEqual(self.current_agreement.is_current, True)

    def test_set_agreement_is_current_as_false_when_addendum_delete(self):
        self.addendum_not_current.save()
        self.assertEqual(self.not_current_agreement.is_current, True)
        self.addendum_not_current.delete()
        self.assertEqual(self.not_current_agreement.is_current, False)

    def test_set_agreement_end_date_actual_as_first_addendum_end_date_when_delete_second_addendum(self):
        self.addendum_current.save()
        self.assertEqual(self.current_agreement.end_date_actual, self.addendum_current.end_date)
        self.second_addendum.save()
        self.assertEqual(self.current_agreement.end_date_actual, self.second_addendum.end_date)
        self.second_addendum.delete()
        self.assertEqual(self.current_agreement.end_date_actual, self.addendum_current.end_date)
