from companies.factories import CompanyFactory
from django.test import TestCase
from invoices.factories import InvoiceFactory
from invoices.models import Invoice
from orders.factories import OrderFactory
from orders.forms.forms_manage_invoices import ManageInvoicesForm


class ManageInvoicesFormTests(TestCase):
    def setUp(self) -> None:
        self.my_company = CompanyFactory.create(is_mine=True)
        self.company_in_order = CompanyFactory.create()
        self.outside_company = CompanyFactory.create()
        self.order = OrderFactory.create(company=self.company_in_order)
        self.income_invoice_original = InvoiceFactory.create(buyer=self.company_in_order, seller=self.my_company)
        self.income_invoice_duplicate = InvoiceFactory.create(
            type=Invoice.DUPLICATE,
            buyer=self.company_in_order,
            seller=self.my_company,
            linked_invoice=self.income_invoice_original,
        )
        self.income_invoice_proforma = InvoiceFactory.create(
            type=Invoice.PROFORMA,
            buyer=self.company_in_order,
            seller=self.my_company,
            linked_invoice=self.income_invoice_original,
        )
        self.cost_invoice_original = InvoiceFactory.create(buyer=self.my_company, seller=self.outside_company)
        self.cost_invoice_duplicate = InvoiceFactory.create(
            type=Invoice.DUPLICATE,
            buyer=self.my_company,
            seller=self.outside_company,
            linked_invoice=self.cost_invoice_original,
        )
        self.cost_invoice_proforma = InvoiceFactory.create(
            type=Invoice.PROFORMA,
            buyer=self.my_company,
            seller=self.outside_company,
            linked_invoice=self.cost_invoice_original,
        )

    def test_form_valid(self):
        form = ManageInvoicesForm(
            instance=self.order,
            data={"cost_invoice": [self.cost_invoice_original.pk], "income_invoice": [self.income_invoice_original.pk]},
        )
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_queryset(self):
        form = ManageInvoicesForm(
            instance=self.order,
            data={"cost_invoice": [self.cost_invoice_original.pk], "income_invoice": [self.income_invoice_original.pk]},
        )
        self.assertTrue(form.is_valid())
        income_invoices_queryset = Invoice.objects.filter(seller__is_mine=True, buyer=self.order.company)
        cost_invoices_queryset = Invoice.objects.filter(buyer__is_mine=True)
        self.assertEqual(list(income_invoices_queryset), list(form.fields["income_invoice"].queryset))
        self.assertEqual(list(cost_invoices_queryset), list(form.fields["cost_invoice"].queryset))

    def test_return_correct_data_order_when_form_save(self):
        form = ManageInvoicesForm(
            instance=self.order,
            data={"cost_invoice": [self.cost_invoice_original.pk], "income_invoice": [self.income_invoice_original.pk]},
        )
        if not form.is_valid():
            print(form.errors)
        order = form.save()
        self.assertEqual(
            list(order.income_invoice.all()),
            list(Invoice.objects.filter(buyer=self.company_in_order, seller=self.my_company)),
        )
        self.assertEqual(
            list(order.cost_invoice.all()),
            list(Invoice.objects.filter(buyer=self.my_company, seller=self.outside_company)),
        )

    def test_get_all_connected_invoices(self):
        form = ManageInvoicesForm(
            instance=self.order,
            data={"cost_invoice": [self.cost_invoice_original.pk], "income_invoice": [self.income_invoice_original.pk]},
        )
        income_invoices = Invoice.objects.filter(pk=self.income_invoice_original.pk)
        all_income_invoices = form.get_all_connected_invoices(invoices=income_invoices)
        expected_value = list(Invoice.objects.filter(buyer=self.company_in_order, seller=self.my_company))
        self.assertEqual(list(all_income_invoices), expected_value)

        cost_invoices = Invoice.objects.filter(pk=self.cost_invoice_original.pk)
        all_cost_invoices = form.get_all_connected_invoices(invoices=cost_invoices)
        expected_value = list(Invoice.objects.filter(buyer=self.my_company, seller=self.outside_company))
        self.assertEqual(list(all_cost_invoices), expected_value)
