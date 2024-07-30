from django.test import TestCase
from employees.factories.factories_salary import SalaryFactory
from employees.forms.forms_salary import SalaryForm
from users.factories import UserFactory


class SalaryFormTests(TestCase):
    def setUp(self) -> None:
        self.salary = SalaryFactory.build()
        self.user = UserFactory.create()

    def test_form_is_valid(self):
        form = SalaryForm(
            data={
                "date": self.salary.date,
                "user": self.user,
                "fee": self.salary.fee,
            }
        )
        self.assertTrue(form.is_valid())
