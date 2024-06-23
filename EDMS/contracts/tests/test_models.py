from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.test import TestCase


class ModelContractTests(TestCase):
    def setUp(self) -> None:
        company = CompanyFactory()
        self.contract = ContractFactory.build(company=company)

    def test_save_address_in_db(self):
        self.contract.save()
        self.assertEqual(Contract.objects.count(), 1)

    def test_return_str(self):
        expected_str = f"{self.contract.name}"
        self.assertEqual(str(self.contract), expected_str)
