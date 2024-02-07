from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from employees.forms.forms_addendum import AddendumForm
from employees.models.models_addendum import Addendum
from employees.models.models_agreement import Agreement
from employees.models.models_termination import Termination


class AddendumCreateView(CreateView):
    model = Addendum
    template_name = "users/addenda/addendum_create.html"
    form_class = AddendumForm

    def get_success_url(self):
        return reverse("detail-addendum", kwargs={"pk": self.object.pk})


class AddendumDetailView(DetailView):
    model = Addendum
    template_name = "users/addenda/addendum_detail.html"


class AddendumUpdateView(UpdateView):
    model = Addendum
    form_class = AddendumForm
    template_name = "users/addenda/addendum_update.html"

    def get_success_url(self):
        return reverse("detail-addendum", kwargs={"pk": self.kwargs["pk"]})

    # TODO
    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        addendum = Addendum.objects.get(pk=self.kwargs["pk"])
        agreement = Agreement.objects.get(pk=addendum.agreement.pk)
        if timezone.now().date() <= agreement.end_date:
            agreement.is_current = True
        else:
            agreement.is_current = False
        agreement.save()
        return super().post(request, *args, **kwargs)


class AddendumDeleteView(DeleteView):
    model = Addendum
    template_name = "users/addenda/addendum_delete.html"

    def get_success_url(self, user_pk: int) -> str:
        return reverse("detail-employee", kwargs={"pk": user_pk})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect:
        addendum: Termination = Addendum.objects.get(pk=self.kwargs["pk"])
        agreement: Agreement = addendum.agreement
        user_pk: int = addendum.agreement.user.pk
        addendum.delete()
        if timezone.now().date() <= agreement.end_date:
            agreement.is_current = True
            agreement.save()
        return redirect(self.get_success_url(user_pk=user_pk))
