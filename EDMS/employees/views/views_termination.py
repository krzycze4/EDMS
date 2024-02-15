from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_termination import TerminationForm
from employees.models.models_termination import Termination


class TerminationCreateView(CreateView, LoginRequiredMixin):
    model = Termination
    template_name = "employees/terminations/termination_create.html"
    form_class = TerminationForm

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.object.pk})


class TerminationDetailView(DetailView, LoginRequiredMixin):
    model = Termination
    template_name = "employees/terminations/termination_detail.html"


class TerminationUpdateView(UpdateView, LoginRequiredMixin):
    model = Termination
    form_class = TerminationForm
    template_name = "employees/terminations/termination_update.html"

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.kwargs["pk"]})


class TerminationDeleteView(DeleteView, LoginRequiredMixin):
    model = Termination
    template_name = "employees/terminations/termination_delete.html"

    def get_success_url(self) -> str:
        return reverse(
            "detail-employee", kwargs={"pk": self.get_object().agreement.user.pk}
        )
