from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from employees.forms.forms_contact import ContactForm
from users.factories import UserFactory


class ContactFormTests(TestCase):
    def setUp(self) -> None:
        self.contact = UserFactory.build()

    def test_if_form_is_valid(self):
        photo = SimpleUploadedFile("test_photo.jpg", b"file_content", content_type="image/jpeg")
        form = ContactForm(
            data={
                "first_name": self.contact.first_name,
                "last_name": self.contact.last_name,
                "email": self.contact.email,
                "phone_number": self.contact.phone_number,
                "position": self.contact.position,
                "photo": photo,
            }
        )
        self.assertTrue(form.is_valid())
