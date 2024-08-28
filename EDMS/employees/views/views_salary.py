from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from employees.filters import SalaryFilterSet
from employees.forms.forms_salary import SalaryForm
from employees.models.models_salaries import Salary


class SalaryCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "employees.add_salary"
    model = Salary
    form_class = SalaryForm
    template_name = "employees/salaries/salary_create.html"

    def get_success_url(self) -> str:
        return reverse("detail-salary", kwargs={"pk": self.object.pk})


class SalaryDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "employees.view_salary"
    model = Salary
    template_name = "employees/salaries/salary_detail.html"


class SalaryUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "employees.change_salary"
    model = Salary
    form_class = SalaryForm
    template_name = "employees/salaries/salary_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-salary", kwargs={"pk": self.object.pk})


class SalaryDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "employees.delete_salary"
    model = Salary
    template_name = "employees/salaries/salary_delete.html"
    success_url = reverse_lazy("list-salary")


class SalaryListView(PermissionRequiredMixin, ListView, LoginRequiredMixin):
    permission_required = "employees.view_salary"
    model = Salary
    ordering = "id"
    paginate_by = 10
    template_name = "employees/salaries/salary_list.html"
    filter_set = None
    context_object_name = "salaries"

    def get_queryset(self) -> QuerySet[Salary]:
        self.filter_set = SalaryFilterSet(
            self.request.GET, queryset=Salary.objects.select_related("user").order_by(self.ordering)
        )
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
