from django.contrib import admin

from .models import Address, Company


class CustomAddressAdmin(admin.ModelAdmin):
    list_display = ("street_name", "street_number", "city", "postcode", "country")


class CustomCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "KRS_id", "REGON_id", "NIP_id")


admin.site.register(Address, CustomAddressAdmin)
admin.site.register(Company, CustomCompanyAdmin)
