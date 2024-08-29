from typing import List

from django import forms
from django.db.models import QuerySet
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
        """
        Initializes the form and sets the queryset for income and cost invoices.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields["income_invoice"].queryset = Invoice.objects.filter(
            seller__is_mine=True, buyer=self.instance.company
        )
        self.fields["cost_invoice"].queryset = Invoice.objects.filter(buyer__is_mine=True)

    def save(self, commit=True) -> Order:
        """
        Saves the form data and updates the order with selected invoices.

        Args:
            commit (bool): Whether to commit the changes to the database. Defaults to True.

        Returns:
            Order: The updated order object.
        """
        order = super().save(commit=commit)

        income_invoices = self.cleaned_data["income_invoice"]
        all_income_invoices = self.get_all_connected_invoices(invoices=income_invoices)

        cost_invoices = self.cleaned_data["cost_invoice"]
        all_cost_invoices = self.get_all_connected_invoices(invoices=cost_invoices)

        order.income_invoice.set(all_income_invoices)
        order.cost_invoice.set(all_cost_invoices)

        return order

    @staticmethod
    def get_all_connected_invoices(invoices: QuerySet[Invoice]) -> List[Invoice]:
        """
        Retrieves all invoices linked to the given invoices.

        Args:
            invoices (QuerySet[Invoice]): The initial set of invoices.

        Returns:
            List[Invoice]: A list of all related invoices.
        """
        linked_invoices = Invoice.objects.filter(linked_invoice__in=invoices)
        all_invoices = list(invoices) + list(linked_invoices)
        return all_invoices
