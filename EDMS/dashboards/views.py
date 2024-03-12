from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .plot_app import app

User = get_user_model()
app = app


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        app.user = request.user
        return super().dispatch(request, *args, **kwargs)
