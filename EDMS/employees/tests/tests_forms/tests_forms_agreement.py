import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.forms.forms_agreement import AgreementForm
from humanize import naturalsize
from users.factories import UserFactory


class AgreementFormTests(TestCase):
    def setUp(self) -> None:
        self.employee = UserFactory.create()
        self.agreement = AgreementFactory.build(user=self.employee)

    def test_form_correct_initials_when_instance_in_kwargs(self):
        form = AgreementForm(instance=self.agreement, user=self.employee)
        self.assertEqual(form.fields["user"].initial, self.agreement.user)
        self.assertEqual(
            form.fields["user_display"].initial, f"{self.agreement.user.first_name} {self.agreement.user.last_name}"
        )

    def test_form_correct_initials_when_instance_not_in_kwargs(self):
        form = AgreementForm(user=self.employee)
        self.assertEqual(form.fields["user"].initial, self.agreement.user)
        self.assertEqual(form.fields["user_display"].initial, f"{self.employee.first_name} {self.employee.last_name}")

    def test_form_is_valid(self):
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": self.agreement.scan,
            },
            files={"scan": self.agreement.scan},
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_agreement_create_date_is_later_than_agreement_start_date(self):
        self.agreement.create_date = self.agreement.start_date + timezone.timedelta(days=1)
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": self.agreement.scan,
            },
            files={"scan": self.agreement.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("Create date must be before or the same as start date.", form.errors["create_date"])

    def test_form_invalid_when_agreement_start_date_is_later_than_agreement_end_date(self):
        self.agreement.start_date = self.agreement.end_date + timezone.timedelta(days=1)
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": self.agreement.scan,
            },
            files={"scan": self.agreement.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End end_date can't be earlier than start end_date!", form.errors["end_date"])

    def test_form_invalid_when_agreement_create_date_is_in_the_future(self):
        self.agreement.create_date = timezone.now().date() + timezone.timedelta(days=1)
        self.agreement.start_date = self.agreement.create_date
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": self.agreement.scan,
            },
            files={"scan": self.agreement.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("The create date can't be future end_date.", form.errors["create_date"])

    def test_form_invalid_when_agreement_scan_extension_is_wrong(self):
        self.agreement.scan = SimpleUploadedFile("test.exe", b"file_content", content_type="application/x-msdownload")
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": self.agreement.scan,
            },
            files={"scan": self.agreement.scan},
        )
        valid_extensions = [
            ".pdf",
            ".jpg",
            ".jpeg",
            ".jfif",
            ".pjpeg",
            ".pjp",
            ".png",
            ".svg",
        ]
        valid_extensions_str = ", ".join(valid_extensions)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(
            f"Incorrect extensions. Your file extension: {os.path.splitext(self.agreement.scan.name)[1]}. Valid extensions: {valid_extensions_str}",
            form.errors["scan"],
        )

    def test_form_invalid_when_agreement_scan_size_is_too_big(self):
        invalid_file = SimpleUploadedFile(
            "test_invalid_file.pdf", b"file_content" * (10**7 + 1), content_type="application/pdf"
        )
        form = AgreementForm(
            user=self.employee,
            data={
                "name": self.agreement.name,
                "type": self.agreement.type,
                "salary_gross": self.agreement.salary_gross,
                "create_date": self.agreement.create_date,
                "start_date": self.agreement.start_date,
                "end_date": self.agreement.end_date,
                "user": self.agreement.user,
                "user_display": self.agreement.user,
                "scan": invalid_file,
            },
            files={"scan": invalid_file},
        )
        max_scan_size: int = 10**7
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(f"Max size file is {naturalsize(max_scan_size)}", form.errors["scan"])
