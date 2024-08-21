import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from humanize import naturalsize
from orders.factories import ProtocolFactory
from orders.forms.forms_protocol import ProtocolForm


class ProtocolFormTest(TestCase):
    def setUp(self) -> None:
        self.protocol = ProtocolFactory.build()

    def test_form_valid(self):
        form = ProtocolForm(
            data={
                "scan": self.protocol.scan,
                "create_date": self.protocol.create_date,
            },
            files={
                "scan": self.protocol.scan,
            },
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_create_date_in_future(self):
        form = ProtocolForm(
            data={
                "scan": self.protocol.scan,
                "create_date": self.protocol.create_date + timezone.timedelta(days=1),
            },
            files={
                "scan": self.protocol.scan,
            },
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("The create date can't be future end_date.", form.errors["create_date"])

    def test_form_invalid_when_scan_extension_is_wrong(self):
        self.protocol.scan = SimpleUploadedFile("test.exe", b"file_content", content_type="application/x-msdownload")
        form = ProtocolForm(
            data={
                "scan": self.protocol.scan,
                "create_date": self.protocol.create_date,
            },
            files={
                "scan": self.protocol.scan,
            },
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
            f"Incorrect extensions. Your file extension: {os.path.splitext(self.protocol.scan.name)[1]}. Valid extensions: {valid_extensions_str}",
            form.errors["scan"],
        )

    def test_form_invalid_when_scan_size_is_too_big(self):
        invalid_file = SimpleUploadedFile(
            "test_invalid_file.pdf", b"file_content" * (10**7 + 1), content_type="application/pdf"
        )
        form = ProtocolForm(
            data={
                "scan": invalid_file,
                "create_date": self.protocol.create_date,
            },
            files={
                "scan": invalid_file,
            },
        )
        max_scan_size: int = 10**7
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(f"Max size file is {naturalsize(max_scan_size)}", form.errors["scan"])
