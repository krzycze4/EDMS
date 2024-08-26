import re
from decimal import Decimal

from companies.models import Company
from contracts.models import Contract
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from invoices.models import Invoice

User = get_user_model()


class Order(models.Model):
    OPEN = "open"
    INVOICING = "invoicing"
    CLOSED = "closed"
    STATUS_CHOICES = [(OPEN, "open"), (INVOICING, "invoicing"), (CLOSED, "closed")]

    name = models.CharField(max_length=15, help_text="Order name, e.g. PLAY-01/01/2024")
    payment = models.DecimalField(
        verbose_name="Payment net price",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal(1.00))],
        help_text="Net price will be earned if order will be completed.",
    )
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default=OPEN, help_text="Order status, one of open, invoicing, closed"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        help_text="The company to which the service is provided.",
    )
    income_invoice = models.ManyToManyField(
        Invoice,
        blank=True,
        related_name="order_from_income_invoice",
        help_text="Income invoices linked with the order.",
    )
    cost_invoice = models.ManyToManyField(
        Invoice, blank=True, related_name="order_from_cost_invoice", help_text="Cost invoices linked with the order."
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Employee who created the order.")
    contract = models.ForeignKey(
        Contract,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        help_text="The contract to which the order is attached.",
    )
    create_date = models.DateField(default=timezone.now().date(), help_text="Creation order date.")
    start_date = models.DateField(help_text="Start order date")
    end_date = models.DateField(help_text="End order date")
    description = models.TextField(
        blank=True, help_text="Description of the order - some necessary information to help complete the order."
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            current_month = timezone.now().strftime("%m")
            current_year = timezone.now().strftime("%Y")
            counter = self.declare_counter(current_month=current_month, current_year=current_year)
            self.name = f"{self.company.shortcut}-{counter}/{current_month}/{current_year}"
        super().save(*args, **kwargs)

    def declare_counter(self, current_month: int, current_year: int) -> int:
        counter = 1
        last_order = Order.objects.filter(
            create_date__month=current_month,
            create_date__year=current_year,
            company=self.company,
        ).last()
        if last_order:
            pattern = re.compile(r"-(\d+)/")
            match = pattern.search(last_order.name)
            counter = int(match.group(1)) + 1
        return counter


class Protocol(models.Model):
    name = models.CharField(max_length=64)
    scan = models.FileField(upload_to="protocols/")
    create_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="protocols")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="protocols")

    def __str__(self) -> str:
        return f"{self.name}"
