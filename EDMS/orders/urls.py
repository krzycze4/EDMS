from django.urls import include, path
from orders.api.views.views_api_orders import OrderModelViewSet
from orders.api.views.views_api_protocols import ProtocolModelViewSet
from orders.views.views_orders import (
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderManageInvoices,
    OrderUpdateView,
)
from orders.views.views_protocols import ProtocolCreateView, ProtocolDeleteView
from rest_framework import routers

router = routers.DefaultRouter()
router.register("api/orders", OrderModelViewSet)
router.register("api/protocols", ProtocolModelViewSet)

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
    path("", include(router.urls)),
]
