from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    ContractCreateView,
    ContractDeleteView,
    ContractDetailView,
    ContractListView,
    ContractUpdateView,
)

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
