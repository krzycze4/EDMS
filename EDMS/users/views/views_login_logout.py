from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from users.forms import CustomAuthenticationForm
from users.models import User


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_invalid(self, form: CustomAuthenticationForm) -> HttpResponse:
        response: HttpResponse = super().form_invalid(form)
        username: str = form.cleaned_data.get("username")
        try:
            user: User = User.objects.get(email=username)
        except User.DoesNotExist:
            messages.error(
                self.request,
                "User does not exist. Please check your email and password.",
            )
        else:
            if not user.is_active:
                messages.warning(
                    self.request,
                    "User is not active. Please check your email and active your account.",
                )
            else:
                messages.warning(self.request, message="Incorrect password!")
        return response


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
