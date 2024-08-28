from datetime import timedelta

from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from contracts.forms import ContractForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from users.factories import UserFactory


class ContractFormTests(TestCase):
    def setUp(self) -> None:
        self.employee = UserFactory()
        self.company = CompanyFactory()
        self.contract = ContractFactory.build(
            company=self.company,
            scan=SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf"),
        )

    def test_form_valid(self):
        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": self.contract.scan,
            },
            files={"scan": self.contract.scan},
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_start_date_after_end_date(self):
        self.contract.start_date = timezone.now().date()
        self.contract.end_date = self.contract.start_date - timedelta(days=1)

        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": self.contract.scan,
            },
            files={"scan": self.contract.scan},
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_file_is_too_big(self):
        big_file = SimpleUploadedFile("big_file.pdf", b"x" * (10**8), content_type="application/pdf")
        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": big_file,
            },
            files={"scan": big_file},
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_file_extension_is_wrong(self):
        invalid_file = SimpleUploadedFile("invalid_file.txt", b"file_content", content_type="text/plain")
        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": invalid_file,
            },
            files={"scan": invalid_file},
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_create_date_is_in_future(self):
        self.contract.create_date = timezone.now().date() + timedelta(days=1)

        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": self.contract.scan,
            },
            files={"scan": self.contract.scan},
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_create_date_after_start_date(self):
        self.contract.create_date = timezone.now().date()
        self.contract.start_date = self.contract.create_date - timedelta(days=1)

        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date,
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": self.contract.scan,
            },
            files={"scan": self.contract.scan},
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_when_create_date_in_future(self):
        self.contract.create_date = timezone.now().date()
        self.contract.start_date = self.contract.create_date - timedelta(days=1)

        form = ContractForm(
            data={
                "name": self.contract.name,
                "create_date": self.contract.create_date + timezone.timedelta(days=1),
                "start_date": self.contract.start_date,
                "end_date": self.contract.end_date,
                "company": self.contract.company.id,
                "employee": [self.employee.id],
                "price": self.contract.price,
                "scan": self.contract.scan,
            },
            files={"scan": self.contract.scan},
        )
        self.assertFalse(form.is_valid())
