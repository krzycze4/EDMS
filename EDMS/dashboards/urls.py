from django.urls import path

from .views import (
    CreateCompanyDoneView,
    CreateCompanyView,
    DashboardView,
    FindCompanyView,
    ListCompanyView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("company/find/", FindCompanyView.as_view(), name="find_company"),
    path("company/create/", CreateCompanyView.as_view(), name="create_company"),
    path(
        "company/create/done",
        CreateCompanyDoneView.as_view(),
        name="create_company_done",
    ),
    path("company/", ListCompanyView.as_view(), name="list_company"),
]
