from django.contrib import admin

from .models import Address, Company, Contact


class CustomAddressAdmin(admin.ModelAdmin):
    list_display = ("street_name", "street_number", "city", "postcode", "country")


class CustomCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "krs", "regon", "nip")


class CustomContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "description")


admin.site.register(Address, CustomAddressAdmin)
admin.site.register(Company, CustomCompanyAdmin)
admin.site.register(Contact, CustomContactAdmin)
