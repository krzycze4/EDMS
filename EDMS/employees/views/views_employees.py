from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from employees.filters import UserFilterSet
from employees.forms.forms_contact import ContactForm
from employees.models.models_addendum import Addendum
from employees.models.models_agreement import Agreement
from employees.models.models_termination import Termination
from employees.models.models_vacation import Vacation

User = get_user_model()


class EmployeeDetailView(DetailView):
    model = User
    template_name = "employees/employees/employee_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agreements"] = Agreement.objects.filter(user=self.object)
        context["vacations"] = Vacation.objects.filter(leave_user=self.object)
        context["terminations"] = Termination.objects.filter(
            agreement__user=self.object
        )
        context["addenda"] = Addendum.objects.filter(agreement__user=self.object)
        return context


class EmployeeUpdateView(UpdateView):
    model = User
    form_class = ContactForm
    template_name = "employees/employees/employee_update.html"

    def get_success_url(self):
        return reverse("detail-employee", kwargs={"pk": self.object.pk})


class EmployeeListView(ListView):
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
