from django.urls import path

from .views import (
    CreateCompanyDoneView,
    CreateCompanyView,
    DetailCompanyView,
    FindCompanyView,
    ListCompanyView,
)

urlpatterns = [
    path("find/", FindCompanyView.as_view(), name="find_company"),
    path("create/", CreateCompanyView.as_view(), name="create_company"),
    path(
        "create/done/",
        CreateCompanyDoneView.as_view(),
        name="create_company_done",
    ),
    path("", ListCompanyView.as_view(), name="list_company"),
    path("<int:pk>/", DetailCompanyView.as_view(), name="detail_company"),
]
