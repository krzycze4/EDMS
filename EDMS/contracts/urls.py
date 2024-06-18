from contracts.api.views_api_contract import ContractModelViewSet
from contracts.views import (
    ContractCreateView,
    ContractDeleteView,
    ContractDetailView,
    ContractListView,
    ContractUpdateView,
)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register("api/contracts", ContractModelViewSet)

urlpatterns = [
    path("contracts/create/", ContractCreateView.as_view(), name="create-contract"),
    path("contracts/<int:pk>/", ContractDetailView.as_view(), name="detail-contract"),
    path(
        "contracts/<int:pk>/update/",
        ContractUpdateView.as_view(),
        name="update-contract",
    ),
    path(
        "contracts/<int:pk>/delete/",
        ContractDeleteView.as_view(),
        name="delete-contract",
    ),
    path("contracts/", ContractListView.as_view(), name="list-contract"),
    path("", include(router.urls)),
]
