from django.test import TestCase
from employees.factories.factories_vacation import VacationFactory
from employees.models.models_vacation import Vacation


class VacationFactoryTests(TestCase):
    def test_create_correct_vacation(self):
        VacationFactory.create()
        self.assertEqual(Vacation.objects.count(), 1)

    def test_create_correct_vacation_bulk(self):
        VacationFactory.create_batch(10)
        self.assertEqual(Vacation.objects.count(), 10)
