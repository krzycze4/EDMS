from django.urls import path

from .views import (
    ActivateAccountView,
    CustomLoginView,
    SuccessRegisterView,
    UserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("", CustomLoginView.as_view(), name="login"),
    path("success-register/", SuccessRegisterView.as_view(), name="success_register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate_account",
    ),
]
