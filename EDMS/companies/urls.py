from django.urls import path

from .views.views_company import (
    CompanyAddressUpdateView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyFindView,
    CompanyIdentifiersUpdateView,
    CompanyListView,
    CreateCompanyDoneView,
)
from .views.views_contact import ContactCreateView, ContactDeleteView, ContactUpdateView

urlpatterns = [
    path("companies/find/", CompanyFindView.as_view(), name="find-company"),
    path("companies/create/", CompanyCreateView.as_view(), name="create-company"),
    path(
        "companies/create/done/",
        CreateCompanyDoneView.as_view(),
        name="create-company-done",
    ),
    path("companies/", CompanyListView.as_view(), name="list-company"),
    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="detail-company"),
    path(
        "companies/<int:pk>/update-identifiers/",
        CompanyIdentifiersUpdateView.as_view(),
        name="update-identifiers",
    ),
    path(
        "companies/<int:pk>/update-address/",
        CompanyAddressUpdateView.as_view(),
        name="update-address",
    ),
    path(
        "companies/<int:pk>/create-contact/",
        ContactCreateView.as_view(),
        name="create-contact",
    ),
    path(
        "companies/<int:company_pk>/update-contact/<int:contact_pk>/",
        ContactUpdateView.as_view(),
        name="update-contact",
    ),
    path(
        "companies/<int:company_pk>/delete-contact/<int:contact_pk>/",
        ContactDeleteView.as_view(),
        name="delete-contact",
    ),
]
