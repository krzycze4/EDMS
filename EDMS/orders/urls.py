from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderManageInvoices,
    OrderUpdateView,
    ProtocolCreateView,
    ProtocolDeleteView,
)

urlpatterns = [
    path("orders/create/", OrderCreateView.as_view(), name="create-order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="detail-order"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="update-order"),
    path("orders/", OrderListView.as_view(), name="list-order"),
    path(
        "orders/<int:pk>/manage-invoices/",
        OrderManageInvoices.as_view(),
        name="manage-invoice",
    ),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="delete-order"),
    path(
        "orders/<int:pk>/add-protocol/",
        ProtocolCreateView.as_view(),
        name="create-protocol",
    ),
    path(
        "orders/protocols/<int:pk>/delete",
        ProtocolDeleteView.as_view(),
        name="delete-protocol",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
