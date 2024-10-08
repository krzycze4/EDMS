# ruff: noqa: F401
from dashboards.plots import render_plot_for_user_group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/dashboard.html"
    permission_required = "dashboards.view_dashboard"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for the dashboard page.
        If user group is not ceos or managers forbid to enter endpoint.

        Args:
            request (HttpRequest): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse | HttpResponseForbidden: The HTTP response with the dashboard or a forbidden response.
        """
        user = request.user
        if user.groups.filter(name__in=["ceos", "managers"]).exists():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plot"] = render_plot_for_user_group(user=self.request.user)
        return context
