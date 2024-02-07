from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


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


admin.site.register(User, CustomUserAdmin)
