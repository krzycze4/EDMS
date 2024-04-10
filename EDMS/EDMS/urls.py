from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("dashboards.urls")),
    path("", include("companies.urls")),
    path("", include("contracts.urls")),
    path("", include("invoices.urls")),
    path("", include("orders.urls")),
    path("", include("employees.urls")),
]

urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
