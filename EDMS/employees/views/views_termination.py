from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_termination import TerminationForm
from employees.models.models_termination import Termination


class TerminationCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "employees.add_termination"
    model = Termination
    template_name = "employees/terminations/termination_create.html"
    form_class = TerminationForm

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.object.pk})


class TerminationDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "employees.view_termination"
    model = Termination
    template_name = "employees/terminations/termination_detail.html"


class TerminationUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "employees.change_termination"
    model = Termination
    form_class = TerminationForm
    template_name = "employees/terminations/termination_update.html"

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.kwargs["pk"]})


class TerminationDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "employees.delete_termination"
    model = Termination
    template_name = "employees/terminations/termination_delete.html"

    def get_success_url(self) -> str:
        return reverse(
            "detail-employee", kwargs={"pk": self.get_object().agreement.user.pk}
        )
