from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.views_addendum import (
    AddendumCreateView,
    AddendumDeleteView,
    AddendumDetailView,
    AddendumUpdateView,
)
from .views.views_address import UserAddressCreateView, UserAddressUpdateView
from .views.views_agreement import (
    AgreementCreateView,
    AgreementDeleteView,
    AgreementDetailView,
    AgreementUpdateView,
)
from .views.views_login_logout import CustomLoginView, CustomLogoutView
from .views.views_register import (
    ActivateAccountView,
    SuccessRegisterView,
    UserRegisterView,
)
from .views.views_reset_password import (
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
)
from .views.views_termination import (
    TerminationCreateView,
    TerminationDeleteView,
    TerminationDetailView,
    TerminationUpdateView,
)
from .views.views_user import UserDetailView, UserListView, UserUpdateView
from .views.views_vacation import (
    VacationCreateView,
    VacationDeleteView,
    VacationDetailView,
    VacationUpdateView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("success-register/", SuccessRegisterView.as_view(), name="success-register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path("forgot-password/", CustomPasswordResetView.as_view(), name="forgot-password"),
    path(
        "forgot-password/done/",
        CustomPasswordResetDoneView.as_view(),
        name="forgot-password-done",
    ),
    path(
        "forgot-password/<str:uidb64>/<str:token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="forgot-password-confirm",
    ),
    path(
        "forgot-password/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="forgot-password-complete",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="detail-user"),
    path(
        "users/<int:pk>/update/", UserUpdateView.as_view(), name="update-user-contact"
    ),
    path(
        "users/<int:pk>/create-address/",
        UserAddressCreateView.as_view(),
        name="create-user-address",
    ),
    path(
        "users/<int:pk>/update-address/",
        UserAddressUpdateView.as_view(),
        name="update-user-address",
    ),
    path(
        "users/<int:pk>/create-agreement/",
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
    path("users/", UserListView.as_view(), name="list-user"),
    path(
        "users/<int:pk>/create-vacation/",
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
        "users/<int:pk>/create-termination/",
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
        "users/<int:pk>/create-addendum/",
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
