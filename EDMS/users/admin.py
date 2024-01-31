from django.contrib import admin

from .models import Agreement, User


class CustomUserAdmin(admin.ModelAdmin):
    exclude = ("password",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )


class CustomAgreementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "salary_gross",
        "start_date",
        "end_date",
        "user",
        "is_current",
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Agreement, CustomAgreementAdmin)
