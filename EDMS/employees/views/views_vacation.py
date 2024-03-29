from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_vacation import VacationForm
from employees.models.models_vacation import Vacation

User = get_user_model()


class VacationCreateView(CreateView, LoginRequiredMixin):
    model = Vacation
    form_class = VacationForm
    template_name = "employees/vacations/vacation_create.html"

    def get_success_url(self) -> None:
        return reverse("detail-vacation", kwargs={"pk": self.object.pk})

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        leave_user = User.objects.get(pk=self.kwargs["pk"])
        initial["leave_user"] = leave_user.pk
        initial["leave_user_display"] = leave_user
        return initial


class VacationDetailView(DetailView, LoginRequiredMixin):
    model = Vacation
    template_name = "employees/vacations/vacation_detail.html"


class VacationUpdateView(UpdateView, LoginRequiredMixin):
    model = Vacation
    form_class = VacationForm
    template_name = "employees/vacations/vacation_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-vacation", kwargs={"pk": self.object.pk})

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        vacation = Vacation.objects.get(pk=self.kwargs["pk"])
        initial["leave_user"] = vacation.leave_user.pk
        initial["leave_user_display"] = vacation.leave_user
        return initial


class VacationDeleteView(DeleteView, LoginRequiredMixin):
    model = Vacation
    template_name = "employees/vacations/vacation_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.object.leave_user.pk})
