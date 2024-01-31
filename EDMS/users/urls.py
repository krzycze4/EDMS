from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

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
from .views.views_user import (
    UserAddressCreateView,
    UserAddressUpdateView,
    UserAgreementCreateView,
    UserAgreementDeleteView,
    UserAgreementDetailView,
    UserAgreementUpdateView,
    UserDetailView,
    UserListView,
    UserUpdateView,
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
        UserAgreementCreateView.as_view(),
        name="create-agreement",
    ),
    path(
        "agreements/<int:pk>/",
        UserAgreementDetailView.as_view(),
        name="detail-agreement",
    ),
    path(
        "agreements/<int:pk>/update/",
        UserAgreementUpdateView.as_view(),
        name="update-agreement",
    ),
    path(
        "agreements/<int:pk>/delete/",
        UserAgreementDeleteView.as_view(),
        name="delete-agreement",
    ),
    path("users/", UserListView.as_view(), name="list-user"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
