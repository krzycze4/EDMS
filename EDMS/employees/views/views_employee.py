from typing import Any, Dict

from dashboards.plots import render_plot
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from employees.filters import UserFilterSet
from employees.forms.forms_contact import ContactForm
from employees.models.models_addendum import Addendum
from employees.models.models_termination import Termination
from orders.models import Order

User = get_user_model()


class EmployeeDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "users.view_user"
    model = User
    template_name = "employees/employees/employee_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_termination"] = Termination.objects.filter(
            agreement__user__id=self.kwargs["pk"]
        ).exists()
        context["has_addendum"] = Addendum.objects.filter(
            agreement__user__id=self.kwargs["pk"]
        ).exists()

        user = get_object_or_404(User, pk=self.kwargs["pk"])

        text_employee = f"Statistics employee: {user}"
        orders_employee = list(
            Order.objects.filter(contract__employee__exact=user).order_by("end_date")
        )

        text_company = "Statistics my company"
        orders_company = list(Order.objects.order_by("end_date"))

        context["plot_employee"] = render_plot(
            orders=orders_employee, text=text_employee
        )

        context["plot_company"] = render_plot(
            orders=orders_company, text=text_company, is_company=True
        )
        is_accountant_or_hr = False
        if user.groups.exists() and user.groups.first().name in ("accountants", "hrs"):
            is_accountant_or_hr = True
        context["is_accountant_or_hr"] = is_accountant_or_hr
        return context


class EmployeeUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "users.change_user"
    model = User
    form_class = ContactForm
    template_name = "employees/employees/employee_update.html"

    def get_success_url(self):
        return reverse("detail-employee", kwargs={"pk": self.object.pk})


class EmployeeListView(PermissionRequiredMixin, ListView, LoginRequiredMixin):
    permission_required = "users.view_user"
    queryset = User.objects.all()
    template_name = "employees/employees/employee_list.html"
    paginate_by = 10
    context_object_name = "users"
    ordering = "last_name"
    filter_set = None

    def get_queryset(self) -> QuerySet[User]:
        queryset = super().get_queryset()
        self.filter_set = UserFilterSet(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
