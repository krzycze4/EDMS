from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
from employees.forms.forms_password import CustomPasswordChangeForm


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "employees/passwords/change_password.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.request.user.pk})
