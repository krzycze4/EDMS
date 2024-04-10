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
    name = models.CharField(max_length=50, blank=False, unique=True)
    seller = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, related_name="seller_invoices")
    buyer = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, related_name="buyer_invoices")
    net_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=False)
    vat = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=False)
    gross = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    create_date = models.DateField(blank=False)
    service_date = models.DateField(blank=False)
    payment_date = models.DateField(blank=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=ORIGINAL)
    linked_invoice = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    scan = models.FileField(upload_to="invoices/")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
