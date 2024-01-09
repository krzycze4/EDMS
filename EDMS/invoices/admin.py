from django.contrib import admin
from invoices.models import Invoice


class CustomInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "seller",
        "buyer",
        "net_price",
        "vat",
        "gross",
        "create_date",
        "service_date",
        "payment_date",
        "is_paid",
    )


admin.site.register(Invoice, CustomInvoiceAdmin)
