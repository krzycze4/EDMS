from _decimal import Decimal
from contracts.api.serializers import ContractSerializer
from contracts.factories import ContractFactory
from contracts.models import Contract
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class ContractSerializerTests(TestCase):
    def setUp(self) -> None:
        self.contract = ContractFactory.create()
        self.contract_data = {
            "id": self.contract.id,
            "name": self.contract.name,
            "create_date": self.contract.create_date.strftime("%Y-%m-%d"),
            "start_date": self.contract.start_date.strftime("%Y-%m-%d"),
            "end_date": self.contract.end_date.strftime("%Y-%m-%d"),
            "price": int(self.contract.price),
            "scan": self.contract.scan.url,
            "company": self.contract.company.id,
            "employee": [employee.id for employee in self.contract.employee.all()],
        }

    def test_contract_serialization(self):
        serializer = ContractSerializer(instance=self.contract)
        self.assertEqual(serializer.data, self.contract_data)

    def test_contract_deserialization(self):
        self.contract.delete()

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
