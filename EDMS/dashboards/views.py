# ruff: noqa: F401
from dashboards.plots import render_plot_for_user_group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    # PermissionRequiredMixin,
    template_name = "dashboards/dashboard.html"
    permission_required = "dashboards.view_dashboard"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name__in=["ceos", "managers"]).exists():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plot"] = render_plot_for_user_group(user=self.request.user)
        return context
