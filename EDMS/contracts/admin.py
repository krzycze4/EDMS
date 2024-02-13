from django.contrib import admin

from .models import Contract


class CustomContractAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "create_date", "company", "price")


admin.site.register(Contract, CustomContractAdmin)
