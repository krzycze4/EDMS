from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_termination import TerminationFactory
from employees.forms.forms_addendum import AddendumForm


class AddendumFormTests(TestCase):
    def setUp(self) -> None:
        agreement = AgreementFactory.create()
        self.addendum = AddendumFactory.build(agreement=agreement)

    def test_form_valid(self):
        form = AddendumForm(
            data={
                "name": self.addendum.name,
                "create_date": self.addendum.create_date,
                "agreement": self.addendum.agreement,
                "end_date": self.addendum.end_date,
                "salary_gross": self.addendum.salary_gross,
                "scan": self.addendum.scan,
            },
            files={"scan": self.addendum.scan},
        )
        self.assertTrue(form.is_valid())

    def test_if_in_form_is_field_agreement_when_addendum_is_not_created(self):
        self.addendum.save()
        form = AddendumForm()
        self.assertFalse(form.fields["agreement"].disabled)

    def test_if_in_form_is_not_field_agreement_when_addendum_is_already_created(self):
        self.addendum.save()
        form = AddendumForm(instance=self.addendum)
        self.assertTrue(form.fields["agreement"].disabled)

    def test_if_field_agreement_queryset_excludes_teriminated_agreements(self):
        form = AddendumForm()
        terminated_agreement = AgreementFactory.create()
        TerminationFactory.create(agreement=terminated_agreement)
        queryset = form.fields["agreement"].queryset
        self.assertIn(self.addendum.agreement, queryset)
        self.assertNotIn(terminated_agreement, queryset)

    def test_form_invalid_when_addendum_end_date_is_earlier_than_agreement_start_date(self):
        self.addendum.end_date = self.addendum.agreement.start_date - timezone.timedelta(days=1)
        form = AddendumForm(
            data={
                "name": self.addendum.name,
                "create_date": self.addendum.create_date,
                "agreement": self.addendum.agreement,
                "end_date": self.addendum.end_date,
                "salary_gross": self.addendum.salary_gross,
                "scan": self.addendum.scan,
            },
            files={"scan": self.addendum.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End date can't be earlier than start date of the agreement.", form.errors["end_date"])

    def test_form_invalid_when_addendum_create_date_is_later_than_addendum_end_date(self):
        self.addendum.create_date = self.addendum.end_date + timezone.timedelta(days=1)
        form = AddendumForm(
            data={
                "name": self.addendum.name,
                "create_date": self.addendum.create_date,
                "agreement": self.addendum.agreement,
                "end_date": self.addendum.end_date,
                "salary_gross": self.addendum.salary_gross,
                "scan": self.addendum.scan,
            },
            files={"scan": self.addendum.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End date can't be earlier than create date of the addendum.", form.errors["end_date"])

    def test_form_invalid_when_addendum_create_date_is_earlier_than_agreement_start_date(self):
        self.addendum.create_date = self.addendum.agreement.start_date - timezone.timedelta(days=1)
        form = AddendumForm(
            data={
                "name": self.addendum.name,
                "create_date": self.addendum.create_date,
                "agreement": self.addendum.agreement,
                "end_date": self.addendum.end_date,
                "salary_gross": self.addendum.salary_gross,
                "scan": self.addendum.scan,
            },
            files={"scan": self.addendum.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("Create date can't be earlier than start date of the agreement.", form.errors["create_date"])

    def test_form_invalid_when_addendum_end_date_is_earlier_than_agreement_end_date_actual(self):
        self.addendum.end_date = self.addendum.agreement.end_date_actual - timezone.timedelta(days=1)
        form = AddendumForm(
            data={
                "name": self.addendum.name,
                "create_date": self.addendum.create_date,
                "agreement": self.addendum.agreement,
                "end_date": self.addendum.end_date,
                "salary_gross": self.addendum.salary_gross,
                "scan": self.addendum.scan,
            },
            files={"scan": self.addendum.scan},
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn(
            "End date addendum can't be earlier than actual end date of the agreement.", form.errors["end_date"]
        )
