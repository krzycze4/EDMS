from companies.models import Address
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from users.forms import AddressForm
from users.models import User


class UserAddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = "users/address/address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form: AddressForm):
        street_name: str = form.cleaned_data["street_name"]
        street_number: str = form.cleaned_data["street_number"]
        city: str = form.cleaned_data["city"]
        postcode: str = form.cleaned_data["postcode"]
        country: str = form.cleaned_data["country"]
        user = User.objects.get(pk=self.kwargs["pk"])
        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )
        user.address = address
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class UserAddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "users/address/address_update.html"

    def get_success_url(self) -> str:
        return reverse("detail-user", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs["pk"])
        return Address.objects.get(pk=user.address.pk)

    def form_valid(self, form):
        street_name: str = form.cleaned_data["street_name"]
        street_number: str = form.cleaned_data["street_number"]
        city: str = form.cleaned_data["city"]
        postcode: str = form.cleaned_data["postcode"]
        country: str = form.cleaned_data["country"]
        user = User.objects.get(pk=self.kwargs["pk"])
        address, created = Address.objects.get_or_create(
            street_name=street_name,
            street_number=street_number,
            city=city,
            postcode=postcode,
            country=country,
        )
        if User.objects.filter(address=user.address).count() == 1:
            user.address.delete()
        user.address = address
        user.save()
        return HttpResponseRedirect(self.get_success_url())
