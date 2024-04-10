from django import forms
from invoices.models import Invoice
from orders.models import Order


class ManageInvoicesForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["cost_invoice", "income_invoice"]
        widgets = {
            "cost_invoice": forms.SelectMultiple(attrs={"class": "form-control js-example-basic-multiple", "size": 3}),
            "income_invoice": forms.SelectMultiple(
                attrs={"class": "form-control js-example-basic-multiple", "size": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.company.is_mine:
            # self.fields.add("invoice")
            self.fields["income_invoice"].widget = forms.SelectMultiple(
                attrs={"class": "form-control  js-example-basic-multiple", "size": 3}
            )
            self.fields["income_invoice"].queryset = Invoice.objects.filter(
                seller__is_mine=True, buyer=self.instance.company
            )
        self.fields["cost_invoice"].queryset = Invoice.objects.filter(buyer__is_mine=True)

    def aggregate_linked_invoices(self):
        family_income_invoices = []
        chosen_income_invoices = list(self.cleaned_data["income_invoice"])
        family_income_invoices.extend(chosen_income_invoices)
        for income_invoice in family_income_invoices:
            if income_invoice.linked_invoice and income_invoice.linked_invoice not in family_income_invoices:
                family_income_invoices.append(income_invoice.linked_invoice)
            children_income_invoices = list(Invoice.objects.filter(linked_invoice=income_invoice))
            if children_income_invoices:
                for children_income_invoice in children_income_invoices:
                    if children_income_invoice not in family_income_invoices:
                        family_income_invoices.append(children_income_invoice)
        return family_income_invoices

    def save(self, commit=True):
        order = super().save(commit=commit)
        family_income_invoices = self.aggregate_linked_invoices()
        income_invoices = Invoice.objects.filter(pk__in=[invoice.pk for invoice in family_income_invoices])
        order.income_invoice.set(income_invoices)
        return order
