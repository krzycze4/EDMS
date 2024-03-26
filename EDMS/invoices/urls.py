from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.views_api_invoice import (
    InvoiceListCreateAPIView,
    InvoiceRetrieveUpdateDestroyAPIView,
)
from .views.views_invoice import (
    InvoiceCreateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
    InvoiceUpdateView,
)

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
    path(
        "api/invoices/",
        InvoiceListCreateAPIView.as_view(),
        name="api-list-create-invoice",
    ),
    path(
        "api/invoices/<int:pk>",
        InvoiceRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-invoice",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
