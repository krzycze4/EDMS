from typing import Any, Dict

from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from users.filters import UserFilter
from users.forms import UserContactUpdateForm
from users.models import Addendum, Agreement, Termination, User, Vacation


class UserDetailView(DetailView):
    model = User
    template_name = "users/users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agreements"] = Agreement.objects.filter(user=self.object)
        context["vacations"] = Vacation.objects.filter(leave_user=self.object)
        # context["left_vacation_days"] = self.count_left_vacation_days()
        context["terminations"] = Termination.objects.filter(
            agreement__user=self.object
        )
        context["addenda"] = Addendum.objects.filter(agreement__user=self.object)
        context["last_addendum"] = (
            Addendum.objects.filter(agreement__user=self.object)
            .order_by("create_date")
            .last()
        )
        return context

    # def count_left_vacation_days(self):
    #     agreements = Agreement.objects.filter(
    #         user=self.object, type=Agreement.EMPLOYMENT
    #     )
    #     return "left_vacation"


class UserUpdateView(UpdateView):
    model = User
    form_class = UserContactUpdateForm
    template_name = "users/users/user_update.html"

    def get_success_url(self):
        return reverse("detail-user", kwargs={"pk": self.object.pk})


class UserListView(ListView):
    queryset = User.objects.all()
    template_name = "users/users/user_list.html"
    paginate_by = 10
    context_object_name = "users"
    ordering = "last_name"
    filter_set = None

    def get_queryset(self) -> QuerySet[User]:
        queryset = super().get_queryset()
        self.filter_set = UserFilter(self.request.GET, queryset=queryset)
        return self.filter_set.qs

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["filter_form"] = self.filter_set.form
        return context
