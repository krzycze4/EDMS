from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CustomUserCreationForm


class UserRegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Registered successfully.")
        return super().form_valid(form)
