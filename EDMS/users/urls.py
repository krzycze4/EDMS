from django.urls import path

from .views import (
    ActivateAccountView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
    SuccessRegisterView,
    UserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("success-register/", SuccessRegisterView.as_view(), name="success_register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate_account",
    ),
    path("forgot-password/", CustomPasswordResetView.as_view(), name="forgot_password"),
    path(
        "forgot-password/done/",
        CustomPasswordResetDoneView.as_view(),
        name="forgot_password_done",
    ),
    path(
        "forgot-password/<str:uidb64>/<str:token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="forgot_password_confirm",
    ),
    path(
        "forgot-password/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="forgot_password_complete",
    ),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
