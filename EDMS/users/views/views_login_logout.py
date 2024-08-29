from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from users.forms.forms_custom_authentication import CustomAuthenticationForm

User = get_user_model()


@method_decorator(ratelimit(key="ip", rate="10/m"), name="post")
class CustomLoginView(LoginView):
    template_name = "users/login_logout/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Determines the URL to redirect to after a successful login based on user groups.

        Returns:
            str: The URL to redirect to after login.
        """
        if self.request.user.groups.filter(name="hrs").exists():
            return reverse_lazy("list-employee")
        elif self.request.user.groups.filter(name="accountants").exists():
            return reverse_lazy("list-invoice")
        else:
            return super().get_success_url()

    def form_invalid(self, form: CustomAuthenticationForm) -> HttpResponse:
        """
        Handles the case where the login form is invalid. Shows error messages based on the user status.

        Args:
            form (CustomAuthenticationForm): The form that was submitted.

        Returns:
            HttpResponse: The response object to be returned.
        """
        response: HttpResponse = super().form_invalid(form)
        username: str = form.cleaned_data.get("username")
        try:
            user: User = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "Invalid email or password.",
            )
        else:
            if not user.is_active:
                messages.warning(
                    self.request,
                    "Invalid email or password.",
                )
            else:
                messages.warning(self.request, message="Invalid email or password.")
        return response


class CustomLogoutView(LogoutView):
    template_name = "users/login_logout/logout.html"
