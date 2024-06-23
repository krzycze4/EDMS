from contracts.factories import ContractFactory
from contracts.models import Contract
from django.test import TestCase


class ContractFactoryTests(TestCase):
    def test_create_correct_contract(self):
        ContractFactory.create()
        self.assertEqual(Contract.objects.count(), 1)

    def test_create_correct_contract_bulk(self):
        ContractFactory.create_batch(10)
        self.assertEqual(Contract.objects.count(), 10)
