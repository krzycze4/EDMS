from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import UpdateView
from employees.forms.forms_group import GroupForm

User = get_user_model()


class GroupUpdateView(UpdateView):
    model = User
    form_class = GroupForm
    template_name = "employees/groups/group_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.kwargs["pk"]})