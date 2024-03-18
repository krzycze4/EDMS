# ruff: noqa: F401
from django.urls import path

from .plot_app import app
from .views import DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
