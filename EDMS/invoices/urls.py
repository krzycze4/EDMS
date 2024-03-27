from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from invoices.api.views_api_invoice import InvoiceModelViewSet
from invoices.views import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceUpdateView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("api/invoices", InvoiceModelViewSet)

urlpatterns = [
    path("invoices/create/", InvoiceCreateView.as_view(), name="create-invoice"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="detail-invoice"),
    path("invoices/", InvoiceListView.as_view(), name="list-invoice"),
    path(
        "invoices/<int:pk>/update", InvoiceUpdateView.as_view(), name="update-invoice"
    ),
    path(
        "invoices/<int:pk>/delete/", InvoiceDeleteView.as_view(), name="delete-invoice"
    ),
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
