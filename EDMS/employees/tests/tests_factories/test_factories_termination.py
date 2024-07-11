from django.test import TestCase
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_termination import Termination


class TerminationFactoryTests(TestCase):
    def test_create_correct_termination(self):
        TerminationFactory.create()
        self.assertEqual(Termination.objects.count(), 1)

    def test_create_correct_termination_bulk(self):
        TerminationFactory.create_batch(10)
        self.assertEqual(Termination.objects.count(), 10)
