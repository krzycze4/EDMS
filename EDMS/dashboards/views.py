# ruff: noqa: F401

from dashboards.plots import render_plot
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from orders.models import Order

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboards/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        text_employee = f"Statistics employee: {self.request.user}"
        orders_employee = list(
            Order.objects.filter(contract__employee__exact=self.request.user).order_by(
                "end_date"
            )
        )

        text_company = "Statistics my company"
        orders_company = list(Order.objects.order_by("end_date"))

        context["plot_employee"] = render_plot(
            orders=orders_employee, text=text_employee
        )
        context["plot_company"] = render_plot(
            orders=orders_company, text=text_company, is_company=True
        )
        return context
