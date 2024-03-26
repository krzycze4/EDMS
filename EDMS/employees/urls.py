from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.views_addendum import (
    AddendumCreateView,
    AddendumDeleteView,
    AddendumDetailView,
    AddendumUpdateView,
)
from .views.views_address import AddressCreateView, AddressUpdateView
from .views.views_agreement import (
    AgreementCreateView,
    AgreementDeleteView,
    AgreementDetailView,
    AgreementUpdateView,
)
from .views.views_api_addendum import (
    AddendumListCreateAPIView,
    AddendumRetrieveUpdateDestroyAPIView,
)
from .views.views_api_agreement import (
    AgreementListCreateAPIView,
    AgreementRetrieveUpdateDestroyAPIView,
)
from .views.views_api_payment import (
    PaymentListCreateAPIView,
    PaymentRetrieveUpdateDestroyAPIView,
)
from .views.views_api_termination import (
    TerminationListCreateAPIView,
    TerminationRetrieveUpdateDestroyAPIView,
)
from .views.views_api_vacation import (
    VacationListCreateAPIView,
    VacationRetrieveUpdateDestroyAPIView,
)
from .views.views_employee import (
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
)
from .views.views_password import CustomPasswordChangeView
from .views.views_payment import (
    PaymentCreateView,
    PaymentDeleteView,
    PaymentDetailView,
    PaymentListView,
    PaymentUpdateView,
)
from .views.views_termination import (
    TerminationCreateView,
    TerminationDeleteView,
    TerminationDetailView,
    TerminationUpdateView,
)
from .views.views_vacation import (
    VacationCreateView,
    VacationDeleteView,
    VacationDetailView,
    VacationUpdateView,
)

urlpatterns = [
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="detail-employee"),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="update-employee-contact",
    ),
    path(
        "employees/<int:pk>/create-address/",
        AddressCreateView.as_view(),
        name="create-employee-address",
    ),
    path(
        "employees/<int:pk>/update-address/",
        AddressUpdateView.as_view(),
        name="update-employee-address",
    ),
    path(
        "employees/<int:pk>/create-agreement/",
        AgreementCreateView.as_view(),
        name="create-agreement",
    ),
    path(
        "agreements/<int:pk>/",
        AgreementDetailView.as_view(),
        name="detail-agreement",
    ),
    path(
        "agreements/<int:pk>/update/",
        AgreementUpdateView.as_view(),
        name="update-agreement",
    ),
    path(
        "agreements/<int:pk>/delete/",
        AgreementDeleteView.as_view(),
        name="delete-agreement",
    ),
    path("employees/", EmployeeListView.as_view(), name="list-employee"),
    path(
        "employees/<int:pk>/create-vacation/",
        VacationCreateView.as_view(),
        name="create-vacation",
    ),
    path("vacations/<int:pk>/", VacationDetailView.as_view(), name="detail-vacation"),
    path(
        "vacations/<int:pk>/update/",
        VacationUpdateView.as_view(),
        name="update-vacation",
    ),
    path(
        "vacations/<int:pk>/delete/",
        VacationDeleteView.as_view(),
        name="delete-vacation",
    ),
    path(
        "employees/<int:pk>/create-termination/",
        TerminationCreateView.as_view(),
        name="create-termination",
    ),
    path(
        "terminations/<int:pk>/",
        TerminationDetailView.as_view(),
        name="detail-termination",
    ),
    path(
        "terminations/<int:pk>/update/",
        TerminationUpdateView.as_view(),
        name="update-termination",
    ),
    path(
        "terminations/<int:pk>/delete/",
        TerminationDeleteView.as_view(),
        name="delete-termination",
    ),
    path(
        "employees/<int:pk>/create-addendum/",
        AddendumCreateView.as_view(),
        name="create-addendum",
    ),
    path("addenda/<int:pk>/", AddendumDetailView.as_view(), name="detail-addendum"),
    path(
        "addenda/<int:pk>/update/", AddendumUpdateView.as_view(), name="update-addendum"
    ),
    path(
        "addenda/<int:pk>/delete/", AddendumDeleteView.as_view(), name="delete-addendum"
    ),
    path(
        "payments/create/",
        PaymentCreateView.as_view(),
        name="create-payment",
    ),
    path(
        "payments/create/<int:pk>/",
        PaymentUpdateView.as_view(),
        name="update-payment",
    ),
    path(
        "payments/<int:pk>/",
        PaymentDetailView.as_view(),
        name="detail-payment",
    ),
    path(
        "payments/<int:pk>/delete/",
        PaymentDeleteView.as_view(),
        name="delete-payment",
    ),
    path(
        "payments/",
        PaymentListView.as_view(),
        name="list-payment",
    ),
    path(
        "change-password/", CustomPasswordChangeView.as_view(), name="change-password"
    ),
    path(
        "api/addenda/",
        AddendumListCreateAPIView.as_view(),
        name="api-list-create-addendum",
    ),
    path(
        "api/addenda/<int:pk>",
        AddendumRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-addendum",
    ),
    path(
        "api/agreements/",
        AgreementListCreateAPIView.as_view(),
        name="api-list-create-agreement",
    ),
    path(
        "api/agreements/<int:pk>",
        AgreementRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-agreement",
    ),
    path(
        "api/payments/",
        PaymentListCreateAPIView.as_view(),
        name="api-list-create-payment",
    ),
    path(
        "api/payments/<int:pk>",
        PaymentRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-payment",
    ),
    path(
        "api/terminations/",
        TerminationListCreateAPIView.as_view(),
        name="api-list-create-termination",
    ),
    path(
        "api/terminations/<int:pk>",
        TerminationRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-termination",
    ),
    path(
        "api/vacations/",
        VacationListCreateAPIView.as_view(),
        name="api-list-create-vacation",
    ),
    path(
        "api/vacations/<int:pk>",
        VacationRetrieveUpdateDestroyAPIView.as_view(),
        name="api-retrieve-update-destroy-vacation",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
