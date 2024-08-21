from companies.factories import CompanyFactory
from contracts.factories import ContractFactory
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from orders.factories import OrderFactory, ProtocolFactory
from orders.forms.forms_order import OrderCreateForm, OrderUpdateForm


class OrderCreateFormTest(TestCase):
    def setUp(self) -> None:
        self.contract = ContractFactory.create()
        self.order = OrderFactory.build(start_date=self.contract.start_date)

    def test_form_valid(self):
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_end_date_before_start_date(self):
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.start_date - timezone.timedelta(days=1),
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End end_date can't be earlier than start end_date!", form.errors["end_date"])

    def test_form_invalid_when_repetition_order(self):
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        form.save()
        self.assertTrue(form.is_valid())
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("description", form.errors)
        self.assertIn("Order with this data already exists!", form.errors["description"])

    def test_form_invalid_when_create_date_in_future(self):
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date + timezone.timedelta(days=1),
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("create_date", form.errors)
        self.assertIn("The create date can't be future end_date.", form.errors["create_date"])

    def test_form_invalid_when_order_start_date_not_in_contract_period(self):
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": self.contract.company.pk,
                "start_date": self.contract.start_date - timezone.timedelta(days=1),
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("start_date", form.errors)
        self.assertIn("Start date must be in contract period.", form.errors["start_date"])

    def test_form_invalid_when_company_in_order_is_not_company_in_contract(self):
        company = CompanyFactory.create()
        form = OrderCreateForm(
            data={
                "payment": self.order.payment,
                "company": company.pk,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "contract": self.contract.pk,
                "description": self.order.description,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("company", form.errors)
        self.assertIn("Company in order must be the same as company in contract.", form.errors["company"])


class OrderUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.contract = ContractFactory.create()
        self.order = OrderFactory.create(contract=self.contract, start_date=self.contract.start_date)

    def test_form_valid(self):
        form = OrderUpdateForm(
            instance=self.order,
            data={
                "company": self.order.company.pk,
                "payment": 100,
                "status": self.order.status,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "description": self.order.description,
                "contract": self.order.contract.pk,
            },
        )
        self.assertTrue(form.is_valid())

    def test_status_readonly_when_end_date_in_future(self):
        ProtocolFactory.create(order=self.order)
        self.order.end_date = timezone.now().date() + timezone.timedelta(days=1)
        self.order.save()
        form = OrderUpdateForm(instance=self.order)
        self.assertIsInstance(form.fields["status"].widget, forms.TextInput)
        self.assertTrue(form.fields["status"].widget.attrs.get("readonly"))

    def test_status_readonly_when_no_protocol(self):
        self.order.end_date = timezone.now().date() - timezone.timedelta(days=1)
        self.order.save()
        form = OrderUpdateForm(instance=self.order)
        self.assertIsInstance(form.fields["status"].widget, forms.TextInput)
        self.assertTrue(form.fields["status"].widget.attrs.get("readonly"))

    def test_status_select_when_end_date_in_past_and_protocol_exists(self):
        ProtocolFactory.create(order=self.order)
        self.order.end_date = timezone.now().date() - timezone.timedelta(days=1)
        self.order.save()
        form = OrderUpdateForm(instance=self.order)
        self.assertIsInstance(form.fields["status"].widget, forms.Select)

    def test_form_invalid_when_order_start_date_not_in_contract_period(self):
        form = OrderUpdateForm(
            instance=self.order,
            data={
                "company": self.order.company.pk,
                "payment": self.order.payment,
                "status": self.order.status,
                "start_date": self.contract.start_date - timezone.timedelta(days=1),
                "create_date": self.order.create_date,
                "end_date": self.order.end_date,
                "description": self.order.description,
                "contract": self.order.contract.pk,
            },
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("start_date", form.errors)
        self.assertIn("Start date must be in contract period.", form.errors["start_date"])

    def test_form_invalid_when_end_date_before_start_date(self):
        form = OrderUpdateForm(
            instance=self.order,
            data={
                "company": self.order.company.pk,
                "payment": self.order.payment,
                "status": self.order.status,
                "start_date": self.order.start_date,
                "create_date": self.order.create_date,
                "end_date": self.order.start_date - timezone.timedelta(days=1),
                "description": self.order.description,
                "contract": self.order.contract.pk,
            },
        )
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)
        self.assertIn("end_date", form.errors)
        self.assertIn("End end_date can't be earlier than start end_date!", form.errors["end_date"])
