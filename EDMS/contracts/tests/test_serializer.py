from _decimal import Decimal
from contracts.api.serializers import ContractSerializer
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class TestCaseContractSerializer(TestCase):
    def setUp(self) -> None:
        self.contract1 = ContractFactory.create()
        self.contract_data = {
            "id": self.contract1.id,
            "name": self.contract1.name,
            "create_date": self.contract1.create_date,
            "start_date": self.contract1.start_date,
            "end_date": self.contract1.end_date,
            "price": int(self.contract1.price),
            "scan": self.contract1.scan.url,
            "company": self.contract1.company.id,
            "employee": [employee.id for employee in self.contract1.employee.all()],
        }

    def test_contract_serialization(self):
        serializer = ContractSerializer(instance=self.contract1)
        self.assertEqual(serializer.data, self.contract_data)

    def test_contract_deserialization(self):
        self.contract1.delete()

        valid_contract_data = self.contract_data.copy()
        valid_contract_data["price"] = Decimal(valid_contract_data["price"])

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_contract_data["scan"] = fake_file

        serializer = ContractSerializer(data=valid_contract_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Contract.objects.count(), 1)
