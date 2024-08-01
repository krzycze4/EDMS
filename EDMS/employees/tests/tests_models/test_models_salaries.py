from django.test import TestCase
from employees.factories.factories_salary import SalaryFactory
from users.factories import UserFactory


class ModelSalaryTests(TestCase):
    def setUp(self) -> None:
        user = UserFactory.create()
        self.salary = SalaryFactory.build(user=user)

    def test_verbose_name_plural(self):
        self.assertEqual(self.salary._meta.verbose_name_plural, "Salaries")
