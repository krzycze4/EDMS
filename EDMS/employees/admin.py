from django.contrib import admin
from employees.models.models_addendum import Addendum, Agreement
from employees.models.models_termination import Termination
from employees.models.models_vacation import Vacation


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


admin.site.register(Vacation, CustomVacationAdmin)
admin.site.register(Agreement, CustomAgreementAdmin)
admin.site.register(Termination, CustomTerminationAdmin)
admin.site.register(Addendum, CustomAddendumAdmin)
