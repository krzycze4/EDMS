# ruff: noqa: F401
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .dash_apps import company_stats, employee_stats


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/dashboard.html"
