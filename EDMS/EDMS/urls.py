from django.conf import settings
from django.conf.urls.static import static
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


if settings.DEBUG:
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
    urlpatterns.append(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.append(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
