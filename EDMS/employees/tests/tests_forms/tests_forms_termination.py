from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.forms.forms_termination import TerminationForm
from employees.models.models_agreement import Agreement


class TerminationFormTest(TestCase):
    def setUp(self) -> None:
        self.agreement = AgreementFactory.create()
        self.termination = TerminationFactory.build(agreement=self.agreement)

    def test_if_field_agreement_is_disabled_when_termination_is_created(self):
        self.termination.save()
        form = TerminationForm(instance=self.termination)
        self.assertTrue(form.fields["agreement"].disabled)

    def test_correct_agreement_queryset_when_termination_is_not_created(self):
        self.termination.save()
        agreement_without_termination = AgreementFactory.create()
        form = TerminationForm()
        agreements_without_terminations = Agreement.objects.filter(termination=None)
        self.assertTrue(form.fields["agreement"].queryset, agreements_without_terminations)
        self.assertEqual(agreement_without_termination, agreements_without_terminations.first())

    def test_form_valid(self):
        form = TerminationForm(
            data={
                "name": self.termination.name,
                "create_date": self.termination.create_date,
                "agreement": self.agreement,
                "end_date": self.termination.end_date,
                "scan": self.termination.scan,
            },
            files={"scan": self.termination.scan},
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_termination_end_date_is_earlier_than_agreement_start_date(self):
        self.termination.end_date = self.termination.agreement.start_date - timezone.timedelta(days=1)
        form = TerminationForm(
            data={
                "name": self.termination.name,
                "create_date": self.termination.create_date,
                "agreement": self.agreement,
                "end_date": self.termination.end_date,
                "scan": self.termination.scan,
            },
            files={"scan": self.termination.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End date can't be earlier than start date of the agreement.", form.errors["end_date"])

    def test_form_invalid_when_termination_create_date_is_later_than_termination_end_date(self):
        self.termination.create_date = self.termination.end_date + timezone.timedelta(days=1)
        form = TerminationForm(
            data={
                "name": self.termination.name,
                "create_date": self.termination.create_date,
                "agreement": self.agreement,
                "end_date": self.termination.end_date,
                "scan": self.termination.scan,
            },
            files={"scan": self.termination.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End date can't be earlier than create date of the termination.", form.errors["end_date"])

    def test_form_invalid_when_termination_create_date_is_earlier_than_agreement_start_date(self):
        self.termination.create_date = self.termination.agreement.start_date - timezone.timedelta(days=1)
        form = TerminationForm(
            data={
                "name": self.termination.name,
                "create_date": self.termination.create_date,
                "agreement": self.agreement,
                "end_date": self.termination.end_date,
                "scan": self.termination.scan,
            },
            files={"scan": self.termination.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("Create date can't be earlier than start date of the agreement.", form.errors["create_date"])

    def test_form_invalid_when_termination_end_date_is_later_than_not_terminated_agreement_end_date_actual(self):
        self.termination.end_date = self.termination.agreement.end_date_actual + timezone.timedelta(days=1)
        form = TerminationForm(
            data={
                "name": self.termination.name,
                "create_date": self.termination.create_date,
                "agreement": self.agreement,
                "end_date": self.termination.end_date,
                "scan": self.termination.scan,
            },
            files={"scan": self.termination.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn(
            "End date termination can't be later than actual end date of the agreement.", form.errors["end_date"]
        )
