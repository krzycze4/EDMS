from django.urls import include, path
from rest_framework import routers

from .api.views_api_user import UserModelViewSet
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

router = routers.DefaultRouter()
router.register("api/users", UserModelViewSet)

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
    path("", include(router.urls)),
]
