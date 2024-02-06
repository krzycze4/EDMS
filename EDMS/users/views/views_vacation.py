from typing import Any, Dict

from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from users.forms import VacationForm
from users.models import User, Vacation


class VacationCreateView(CreateView):
    model = Vacation
    form_class = VacationForm
    template_name = "users/vacations/vacation_create.html"

    def get_success_url(self) -> None:
        return reverse("detail-vacation", kwargs={"pk": self.object.pk})

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        leave_user = User.objects.get(pk=self.kwargs["pk"])
        initial["leave_user"] = leave_user.pk
        initial["leave_user_display"] = leave_user
        return initial


class VacationDetailView(DetailView):
    model = Vacation
    template_name = "users/vacations/vacation_detail.html"


class VacationUpdateView(UpdateView):
    model = Vacation
    form_class = VacationForm
    template_name = "users/vacations/vacation_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-vacation", kwargs={"pk": self.object.pk})

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        vacation = Vacation.objects.get(pk=self.kwargs["pk"])
        initial["leave_user"] = vacation.leave_user.pk
        initial["leave_user_display"] = vacation.leave_user
        return initial


class VacationDeleteView(DeleteView):
    model = Vacation
    template_name = "users/vacations/vacation_delete.html"

    def get_success_url(self) -> str:
        print(self.object.leave_user.pk)
        return reverse("detail-user", kwargs={"pk": self.object.leave_user.pk})
