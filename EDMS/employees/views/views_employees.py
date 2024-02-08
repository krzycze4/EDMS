from math import ceil
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView
from employees.filters import UserFilter
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
        context["vacations_left"] = (
            self.count_granted_vacation_from_agreement() - self.count_used_vacation()
        )
        return context

    def count_granted_vacation_from_agreement(self) -> int:
        vacation_from_agreement = 0
        current_agreement = Agreement.objects.get(
            user=self.object, is_current=True, type=Agreement.EMPLOYMENT
        )
        if current_agreement:
            months_in_year = 12
            work_months_current_year = self.count_work_months_current_year(
                agreement=current_agreement
            )
            vacation_from_agreement = ceil(
                work_months_current_year
                * self.object.vacation_days_per_year
                / months_in_year
            )
        return vacation_from_agreement

    @staticmethod
    def count_used_vacation() -> int:
        used_vacations_days: int = 0
        vacations = list(Vacation.objects.filter(type=Vacation.ANNUAL))
        for vacation in vacations:
            used_vacations_days += (
                (vacation.end_date - vacation.start_date).days - vacation.days_off + 1
            )
        return used_vacations_days

    @staticmethod
    def count_work_months_current_year(agreement: Agreement = None) -> int:
        if agreement:
            start_month = agreement.start_date.month
            end_month = agreement.end_date_actual.month
            if agreement.start_date.year < timezone.now().year:
                january = 1
                start_month = january
            if agreement.end_date_actual.year > timezone.now().year:
                december = 12
                end_month = december
            return end_month - start_month + 1
        return 0


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
        self.filter_set = UserFilter(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
