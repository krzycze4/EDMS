from decimal import Decimal

from companies.models import Company
from django.core.validators import MinValueValidator
from django.db import models


class Invoice(models.Model):
    ORIGINAL = "original"
    DUPLICATE = "duplicate"
    PROFORMA = "proforma"
    CORRECTING = "correcting"
    TYPE_CHOICES = (
        (ORIGINAL, "original"),
        (DUPLICATE, "duplicate"),
        (PROFORMA, "proforma"),
        (CORRECTING, "correcting"),
    )
    name = models.CharField(max_length=50, blank=False, unique=True, help_text="Invoice name, e.g. PLAY-01-01-2024")
    seller = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=False, related_name="seller_invoices", help_text="Company seller"
    )
    buyer = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=False, related_name="buyer_invoices", help_text="Company buyer"
    )
    net_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        blank=False,
        help_text="Net value",
    )
    vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        blank=False,
        help_text="Vat value",
    )
    gross = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))], help_text="Gross value"
    )
    create_date = models.DateField(blank=False, help_text="Creation date")
    service_date = models.DateField(blank=False, help_text="Service date")
    payment_date = models.DateField(blank=False, help_text="Payment date")
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=ORIGINAL,
        help_text="Invoice type, one of original, duplicate, proforma, correcting.",
    )
    linked_invoice = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="An invoice connected with the invoice, e.g. correcting invoice to original.",
    )
    scan = models.FileField(upload_to="invoices/", help_text="Physical version of the document.")
    is_paid = models.BooleanField(
        default=False, help_text="It tells us if the invoice has been already paid or not yet."
    )

    def __str__(self):
        return f"{self.name}"
