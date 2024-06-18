from django.urls import include, path
from employees.api.views.views_api_agreement import AgreementModelViewSet
from rest_framework import routers

from .api.views.views_api_addendum import AddendumModelViewSet
from .api.views.views_api_payment import SalaryModelViewSet
from .api.views.views_api_termination import TerminationModelViewSet
from .api.views.views_api_vacation import VacationModelViewSet
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
from .views.views_employee import (
    EmployeeDetailView,
    EmployeeListView,
    EmployeeUpdateView,
)
from .views.views_group import GroupUpdateView
from .views.views_password import CustomPasswordChangeView
from .views.views_salary import (
    SalaryCreateView,
    SalaryDeleteView,
    SalaryDetailView,
    SalaryListView,
    SalaryUpdateView,
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

router = routers.DefaultRouter()
router.register("api/addenda", AddendumModelViewSet)
router.register("api/agreements", AgreementModelViewSet)
router.register("api/salaries", SalaryModelViewSet)
router.register("api/terminations", TerminationModelViewSet)
router.register("api/vacations", VacationModelViewSet)

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
    path("addenda/<int:pk>/update/", AddendumUpdateView.as_view(), name="update-addendum"),
    path("addenda/<int:pk>/delete/", AddendumDeleteView.as_view(), name="delete-addendum"),
    path(
        "salaries/create/",
        SalaryCreateView.as_view(),
        name="create-salary",
    ),
    path(
        "salaries/create/<int:pk>/",
        SalaryUpdateView.as_view(),
        name="update-salary",
    ),
    path(
        "salaries/<int:pk>/",
        SalaryDetailView.as_view(),
        name="detail-salary",
    ),
    path(
        "salaries/<int:pk>/delete/",
        SalaryDeleteView.as_view(),
        name="delete-salary",
    ),
    path(
        "salaries/",
        SalaryListView.as_view(),
        name="list-salary",
    ),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change-password"),
    path("employees/<int:pk>/update-group", GroupUpdateView.as_view(), name="update-group"),
    path("", include(router.urls)),
]
