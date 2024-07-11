from django.test import TestCase
from employees.factories.factories_salary import SalaryFactory
from employees.models.models_salaries import Salary


class SalaryFactoryTests(TestCase):
    def test_create_correct_agreement(self):
        SalaryFactory.create()
        self.assertEqual(Salary.objects.count(), 1)

    def test_create_correct_agreement_bulk(self):
        SalaryFactory.create_batch(10)
        self.assertEqual(Salary.objects.count(), 10)
