from companies.forms.forms_contact import CreateContactForm, UpdateContactForm
from companies.models import Company, Contact
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView


class ContactCreateView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = "companies.add_contact"
    model = Contact
    template_name = "companies/contacts/create_contact.html"
    form_class = CreateContactForm

    def get_initial(self):
        company_pk = self.kwargs["pk"]
        company = Company.objects.get(id=company_pk)
        return {"company": company}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        company_pk = self.kwargs["pk"]
        company = Company.objects.get(id=company_pk)
        context["company"] = company
        return context

    def get_success_url(self):
        return reverse("detail-company", kwargs={"pk": self.kwargs["pk"]})


class ContactUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = "companies.change_contact"
    model = Contact
    form_class = UpdateContactForm
    template_name = "companies/contacts/update_contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.get(pk=self.kwargs["company_pk"])
        contact = Contact.objects.get(pk=self.kwargs["contact_pk"])
        context["company"] = company
        context["contact"] = contact
        return context

    def get_initial(self):
        company_pk = self.kwargs["company_pk"]
        company = Company.objects.get(id=company_pk)
        return {"company": company}

    def get_object(self, **kwargs):
        company_pk = self.kwargs["company_pk"]
        contact_pk = self.kwargs["contact_pk"]
        contact = Contact.objects.get(id=contact_pk, company_id=company_pk)
        return contact

    def get_success_url(self):
        return reverse_lazy("detail-company", kwargs={"pk": self.kwargs["company_pk"]})


class ContactDeleteView(PermissionRequiredMixin, DeleteView, LoginRequiredMixin):
    permission_required = "companies.delete_contact"
    model = Contact
    template_name = "companies/contacts/delete_contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_id = self.kwargs["company_pk"]
        company = Company.objects.get(id=company_id)
        context["company"] = company
        return context

    def get_object(self):
        company_pk = self.kwargs["company_pk"]
        contact_pk = self.kwargs["contact_pk"]
        contact = Contact.objects.get(id=contact_pk, company_id=company_pk)
        return contact

    def get_success_url(self):
        return reverse_lazy("detail-company", kwargs={"pk": self.kwargs["company_pk"]})
