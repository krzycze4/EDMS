from django.test import TestCase
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_agreement import Agreement


class AgreementFactoryTests(TestCase):
    def test_create_correct_contract(self):
        AgreementFactory.create()
        self.assertEqual(Agreement.objects.count(), 1)

    def test_create_correct_contract_bulk(self):
        AgreementFactory.create_batch(10)
        self.assertEqual(Agreement.objects.count(), 10)
