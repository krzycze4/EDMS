from django.contrib import admin

from .models import Addendum, Agreement, Termination, User, Vacation


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
        "end_date_actual",
        "user",
        "is_current",
    )


class CustomTerminationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "agreement",
        "create_date",
        "end_date",
    )


class CustomVacationAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "start_date",
        "end_date",
        "leave_user",
    )


class CustomAddendumAdmin(admin.ModelAdmin):
    list_display = ("name", "agreement", "create_date", "end_date", "salary_gross")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Vacation, CustomVacationAdmin)
admin.site.register(Agreement, CustomAgreementAdmin)
admin.site.register(Termination, CustomTerminationAdmin)
admin.site.register(Addendum, CustomAddendumAdmin)
