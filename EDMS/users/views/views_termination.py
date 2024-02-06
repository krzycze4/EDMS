from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from users.forms import TerminationForm
from users.models import Agreement, Termination


class TerminationCreateView(CreateView):
    model = Termination
    template_name = "users/terminations/termination_create.html"
    form_class = TerminationForm

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.object.pk})

    def form_valid(self, form: TerminationForm) -> HttpResponse:
        form.instance.agreement.end_date_actual = form.instance.end_date
        if (
            not form.instance.agreement.is_current
            and form.instance.agreement.end_date_actual < timezone.now().date()
        ):
            form.instance.agreement.is_current = False
        else:
            form.instance.agreement.is_current = True
        form.instance.agreement.save()
        return super().form_valid(form)


class TerminationDetailView(DetailView):
    model = Termination
    template_name = "users/terminations/termination_detail.html"


class TerminationUpdateView(UpdateView):
    model = Termination
    form_class = TerminationForm
    template_name = "users/terminations/termination_update.html"

    def get_success_url(self):
        return reverse("detail-termination", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        termination = Termination.objects.get(pk=self.kwargs["pk"])
        agreement = Agreement.objects.get(pk=termination.agreement.pk)
        if timezone.now().date() <= agreement.end_date:
            agreement.is_current = True
        else:
            agreement.is_current = False
        agreement.save()
        return super().post(request, *args, **kwargs)


class TerminationDeleteView(DeleteView):
    model = Termination
    template_name = "users/terminations/termination_delete.html"

    def get_success_url(self, user_pk: int) -> str:
        return reverse("detail-user", kwargs={"pk": user_pk})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        termination: Termination = Termination.objects.get(pk=self.kwargs["pk"])
        agreement: Agreement = termination.agreement
        user_pk: int = termination.agreement.user.pk
        termination.delete()
        if timezone.now().date() <= agreement.end_date:
            agreement.is_current = True
            agreement.save()
        return redirect(self.get_success_url(user_pk=user_pk))
