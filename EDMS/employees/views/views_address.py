from companies.models import Address
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from employees.forms.forms_address import AddressForm

User = get_user_model()


class AddressCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "companies.add_address"
    model = Address
    form_class = AddressForm
    template_name = "employees/addresses/address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form: AddressForm):
        """
        Handles the form submission if the form is valid.

        Args:
            form (AddressForm): The form containing the address data.

        Returns:
            HttpResponseRedirect: Redirects to the employee's detail page after saving the address.
        """
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        address, created = Address.objects.get_or_create(**form.cleaned_data)
        user.address = address
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class AddressUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "companies.change_address"
    model = Address
    form_class = AddressForm
    template_name = "employees/addresses/address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-employee", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Address.objects.get(pk=user.address.pk)

    def form_valid(self, form):
        """
        Handles the form submission if the form is valid.

        Args:
            form (AddressForm): The form containing the address data.

        Returns:
            HttpResponseRedirect: Redirects to the employee's detail page after saving the address.
        """
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        form.save()
        user.address = form.instance
        user.save()
        return HttpResponseRedirect(self.get_success_url())
