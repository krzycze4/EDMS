import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_vacation import VacationFactory
from employees.forms.forms_vacation import VacationForm
from humanize import naturalsize
from users.factories import UserFactory

User = get_user_model()


class VacationFormTests(TestCase):
    def setUp(self) -> None:
        self.leave_user = UserFactory.create(vacation_left=26)
        self.substitute_users = UserFactory.create_batch(2)
        self.vacation = VacationFactory.build(leave_user=self.leave_user, substitute_users=self.substitute_users)

    def test_field_substitute_users_queryset_exclude_leave_user(self):
        form = VacationForm(initial={"leave_user": self.leave_user.id})
        form_substitute_users_ids = list(form.fields["substitute_users"].queryset.values_list("id", flat=True))
        expected_substitute_users_ids = list(User.objects.exclude(id=self.leave_user.id).values_list("id", flat=True))
        self.assertEqual(form_substitute_users_ids, expected_substitute_users_ids)

    def test_form_valid(self):
        AgreementFactory.create(user=self.leave_user)
        form = VacationForm(
            initial={"leave_user": self.leave_user.id},
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user,
                "leave_user_display": self.leave_user,
                "substitute_users": self.substitute_users,
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertTrue(form.is_valid())

    def test_if_id_is_in_cleaned_data_when_vacation_is_created(self):
        AgreementFactory.create(user=self.leave_user)
        self.vacation.save()
        form = VacationForm(
            instance=self.vacation,
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertTrue(form.is_valid())
        cleaned_data = form.clean()
        self.assertIn("id", cleaned_data)
        self.assertEqual(cleaned_data["id"], self.vacation.id)

    def test_form_invalid_when_overlap_vacation_dates_and_vacation_is_not_created(self):
        AgreementFactory.create(user=self.leave_user)
        existed_vacation = VacationFactory.create(leave_user=self.leave_user, substitute_users=self.substitute_users)
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("start_date", form.errors)
        self.assertIn("The vacation overlaps...", form.errors["start_date"])
        self.assertIn("end_date", form.errors)
        self.assertIn(f"...overlaps vacation #{existed_vacation.pk}", form.errors["end_date"])

    def test_form_invalid_when_overlap_vacation_dates_and_vacation_is_created(self):
        AgreementFactory.create(user=self.leave_user)
        existed_vacation = VacationFactory.create(leave_user=self.leave_user, substitute_users=self.substitute_users)
        form = VacationForm(
            instance=self.vacation,
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("start_date", form.errors)
        self.assertIn("The vacation overlaps...", form.errors["start_date"])
        self.assertIn("end_date", form.errors)
        self.assertIn(f"...overlaps vacation #{existed_vacation.pk}", form.errors["end_date"])

    def test_form_invalid_when_leave_user_has_employment_contract_and_cannot_take_vacation(self):
        create_date = timezone.now().date() - timezone.timedelta(days=2)
        end_date = timezone.now().date() - timezone.timedelta(days=1)
        AgreementFactory.create(
            user=self.leave_user, create_date=create_date, start_date=create_date, end_date=end_date
        )
        self.leave_user.vacation_left += 10
        self.leave_user.save()
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(
            "You can't take vacation because you don't have current employment agreement.", form.errors["scan"]
        )

    def test_form_invalid_when_vacation_duration_is_bigger_than_leave_user_vacation_left(self):
        self.vacation.end_date = self.vacation.end_date + timezone.timedelta(days=100)
        AgreementFactory.create(user=self.leave_user)
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn("You can't take vacation because you don't have enough vacation left.", form.errors["scan"])

    def test_form_invalid_when_vacation_end_date_before_vacation_start_date(self):
        self.vacation.end_date = self.vacation.start_date - timezone.timedelta(days=1)
        AgreementFactory.create(user=self.leave_user)
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End end_date can't be earlier than start end_date!", form.errors["end_date"])

    def test_form_invalid_when_vacation_scan_extension_is_wrong(self):
        self.vacation.scan = SimpleUploadedFile("test.exe", b"file_content", content_type="application/x-msdownload")
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": self.vacation.scan,
            },
            files={"scan": self.vacation.scan},
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
            f"Incorrect extensions. Your file extension: {os.path.splitext(self.vacation.scan.name)[1]}. Valid extensions: {valid_extensions_str}",
            form.errors["scan"],
        )

    def test_form_invalid_when_vacation_scan_size_is_too_big(self):
        AgreementFactory.create(user=self.leave_user)
        invalid_file = SimpleUploadedFile(
            "test_invalid_file.pdf", b"file_content" * (10**7 + 1), content_type="application/pdf"
        )
        form = VacationForm(
            data={
                "type": self.vacation.type,
                "start_date": self.vacation.start_date,
                "end_date": self.vacation.end_date,
                "included_days_off": self.vacation.included_days_off,
                "leave_user": self.leave_user.id,
                "leave_user_display": self.leave_user,
                "substitute_users": [user.id for user in self.substitute_users],
                "scan": invalid_file,
            },
            files={"scan": invalid_file},
        )
        max_scan_size: int = 10**7
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("scan", form.errors)
        self.assertIn(f"Max size file is {naturalsize(max_scan_size)}", form.errors["scan"])
