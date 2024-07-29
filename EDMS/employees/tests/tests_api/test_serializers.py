from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from employees.api.serializers import (
    AddendumSerializer,
    AgreementSerializer,
    SalarySerializer,
    TerminationSerializer,
    VacationSerializer,
)
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_salary import SalaryFactory
from employees.factories.factories_termination import TerminationFactory
from employees.factories.factories_vacation import VacationFactory
from employees.models.models_addendum import Addendum
from employees.models.models_agreement import Agreement
from employees.models.models_salaries import Salary
from employees.models.models_termination import Termination
from employees.models.models_vacation import Vacation
from users.factories import UserFactory


class AddendumSerializerTests(TestCase):
    def setUp(self) -> None:
        agreement = AgreementFactory.create()
        self.addendum = AddendumFactory.create(agreement=agreement)
        self.addendum_data = {
            "id": self.addendum.id,
            "name": self.addendum.name,
            "agreement": agreement.id,
            "create_date": self.addendum.create_date.strftime("%Y-%m-%d"),
            "end_date": self.addendum.end_date.strftime("%Y-%m-%d"),
            "salary_gross": self.addendum.salary_gross,
            "scan": self.addendum.scan.url,
        }

    def test_addendum_serialization(self):
        serializer = AddendumSerializer(instance=self.addendum)
        self.assertEqual(serializer.data, self.addendum_data)

    def test_addendum_deserialization(self):
        self.addendum.delete()

        valid_addendum_data = self.addendum_data.copy()
        valid_addendum_data["salary_gross"] = Decimal(valid_addendum_data["salary_gross"])

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_addendum_data["scan"] = fake_file

        serializer = AddendumSerializer(data=valid_addendum_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Addendum.objects.count(), 1)


class AgreementSerializerTests(TestCase):
    def setUp(self) -> None:
        employee = UserFactory.create()
        self.agreement = AgreementFactory.create(user=employee)
        self.agreement_data = {
            "id": self.agreement.id,
            "name": self.agreement.name,
            "type": self.agreement.type,
            "salary_gross": self.agreement.salary_gross,
            "create_date": self.agreement.create_date.strftime("%Y-%m-%d"),
            "start_date": self.agreement.start_date.strftime("%Y-%m-%d"),
            "end_date": self.agreement.end_date.strftime("%Y-%m-%d"),
            "end_date_actual": self.agreement.end_date_actual.strftime("%Y-%m-%d"),
            "user": employee.id,
            "scan": self.agreement.scan.url,
            "is_current": self.agreement.is_current,
        }

    def test_agreement_serialization(self):
        serializer = AgreementSerializer(instance=self.agreement)
        self.assertEqual(serializer.data, self.agreement_data)

    def test_agreement_deserialization(self):
        self.agreement.delete()

        valid_agreement_data = self.agreement_data.copy()
        valid_agreement_data["salary_gross"] = Decimal(valid_agreement_data["salary_gross"])

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_agreement_data["scan"] = fake_file

        serializer = AgreementSerializer(data=valid_agreement_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Agreement.objects.count(), 1)


class SalarySerializerTests(TestCase):
    def setUp(self) -> None:
        employee = UserFactory.create()
        self.salary = SalaryFactory.create(user=employee)
        self.salary_data = {
            "id": self.salary.id,
            "date": self.salary.date.strftime("%Y-%m-%d"),
            "user": employee.id,
            "fee": self.salary.fee,
        }

    def test_salary_serialization(self):
        serializer = SalarySerializer(instance=self.salary)
        self.assertEqual(serializer.data, self.salary_data)

    def test_salary_deserialization(self):
        self.salary.delete()

        valid_salary_data = self.salary_data.copy()
        valid_salary_data["fee"] = Decimal(valid_salary_data["fee"])

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_salary_data["scan"] = fake_file

        serializer = SalarySerializer(data=valid_salary_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Salary.objects.count(), 1)


class TerminationSerializerTests(TestCase):
    def setUp(self) -> None:
        agreement = AgreementFactory.create()
        self.termination = TerminationFactory.create(agreement=agreement)
        self.termination_data = {
            "id": self.termination.id,
            "name": self.termination.name,
            "agreement": agreement.id,
            "create_date": self.termination.create_date.strftime("%Y-%m-%d"),
            "end_date": self.termination.end_date.strftime("%Y-%m-%d"),
            "scan": self.termination.scan.url,
        }

    def test_termination_serialization(self):
        serializer = TerminationSerializer(instance=self.termination)
        self.assertEqual(serializer.data, self.termination_data)

    def test_termination_deserialization(self):
        self.termination.delete()

        valid_termination_data = self.termination_data.copy()

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_termination_data["scan"] = fake_file

        serializer = TerminationSerializer(data=valid_termination_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Termination.objects.count(), 1)


class VacationSerializerTests(TestCase):
    def setUp(self) -> None:
        leave_user = UserFactory.create()
        substitute_users = UserFactory.create_batch(2)
        self.vacation = VacationFactory.create(leave_user=leave_user, substitute_users=substitute_users)
        self.vacation_data = {
            "id": self.vacation.id,
            "type": self.vacation.type,
            "start_date": self.vacation.start_date.strftime("%Y-%m-%d"),
            "end_date": self.vacation.end_date.strftime("%Y-%m-%d"),
            "leave_user": leave_user.id,
            "substitute_users": [user.id for user in substitute_users],
            "scan": self.vacation.scan.url,
            "included_days_off": self.vacation.included_days_off,
        }

    def test_vacation_serialization(self):
        serializer = VacationSerializer(instance=self.vacation)
        self.assertEqual(serializer.data, self.vacation_data)

    def test_vacation_deserialization(self):
        self.vacation.delete()

        valid_vacation_data = self.vacation_data.copy()

        fake_file = SimpleUploadedFile(
            name="the_file.pdf", content=b"This is a test pdf file content.", content_type="application/pdf"
        )
        valid_vacation_data["scan"] = fake_file

        serializer = VacationSerializer(data=valid_vacation_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(Vacation.objects.count(), 1)
