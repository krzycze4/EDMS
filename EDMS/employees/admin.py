from django.contrib import admin

from .models.models_addendum import Addendum, Agreement
from .models.models_payment import Payment
from .models.models_termination import Termination
from .models.models_vacation import Vacation


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


class CustomPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "user", "fee")


admin.site.register(Vacation, CustomVacationAdmin)
admin.site.register(Agreement, CustomAgreementAdmin)
admin.site.register(Termination, CustomTerminationAdmin)
admin.site.register(Addendum, CustomAddendumAdmin)
admin.site.register(Payment, CustomPaymentAdmin)
