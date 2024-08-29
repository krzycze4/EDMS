from typing import Any, Dict

from dashboards.plots import render_plot_for_user_group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from employees.filters import UserFilterSet
from employees.forms.forms_contact import ContactForm
from employees.models.models_addendum import Addendum
from employees.models.models_termination import Termination

User = get_user_model()


class EmployeeDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "users.view_user"
    model = User
    template_name = "employees/employees/employee_detail.html"

    def get_context_data(self, **kwargs):
        """
        Add extra context data for the employee detail view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data including plots, agreements, terminations, addenda, and vacations.
        """
        context = super().get_context_data(**kwargs)
        context["plot"] = render_plot_for_user_group(user=self.object)
        context["agreements"] = self.object.agreements.all()
        context["terminations"] = Termination.objects.filter(agreement__user__id=self.kwargs["pk"]).select_related(
            "agreement"
        )
        context["addenda"] = Addendum.objects.filter(agreement__user__id=self.kwargs["pk"]).select_related("agreement")
        context["vacations"] = self.object.vacations.prefetch_related("substitute_users")
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
        """
        Get the list of users, applying any filters from the request.

        Returns:
            QuerySet[User]: Filtered list of users based on the request.
        """
        queryset = super().get_queryset()
        self.filter_set = UserFilterSet(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
