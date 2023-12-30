from django.urls import path

from .views import (
    InvoiceCreateView,
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
]
