# ruff: noqa: F401

from dashboards.plots import render_plot_for_user_group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plot"] = render_plot_for_user_group(user=self.request.user)
        return context
