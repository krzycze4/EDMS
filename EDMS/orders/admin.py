from django.contrib import admin

from .models import Order, Protocol


class CustomOrderAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "payment",
        "status",
        "company",
        "user",
        "create_date",
        "start_date",
        "end_date",
    ]


class CustomProtocolAdmin(admin.ModelAdmin):
    list_display = ["name", "create_date", "user", "order"]


admin.site.register(Order, CustomOrderAdmin)
admin.site.register(Protocol, CustomProtocolAdmin)
