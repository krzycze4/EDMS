from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_addendum import AddendumForm
from employees.models.models_addendum import Addendum

User = get_user_model()


class AddendumCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "addendum.add_addendum"
    model = Addendum
    template_name = "employees/addenda/addendum_create.html"
    form_class = AddendumForm

    def get_success_url(self):
        return reverse("detail-addendum", kwargs={"pk": self.object.pk})


class AddendumDetailView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = "addendum.view_addendum"
    model = Addendum
    template_name = "employees/addenda/addendum_detail.html"


class AddendumUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "addendum.change_addendum"
    model = Addendum
    form_class = AddendumForm
    template_name = "employees/addenda/addendum_update.html"

    def get_success_url(self):
        return reverse("detail-addendum", kwargs={"pk": self.kwargs["pk"]})


class AddendumDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "addendum.delete_addendum"
    model = Addendum
    template_name = "employees/addenda/addendum_delete.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.get_object().agreement.user.pk})
