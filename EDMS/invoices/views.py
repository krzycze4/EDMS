from django.db.models import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .filters import InvoiceFilter
from .forms import InvoiceForm
from .models import Invoice


class InvoiceCreateView(CreateView):
    template_name = "invoices/create_invoice.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse_lazy("detail-invoice", kwargs={"pk": self.object.pk})


class InvoiceDetailView(DetailView):
    template_name = "invoices/detail_invoice.html"
    model = Invoice


class InvoiceListView(ListView):
    template_name = "invoices/list_invoice.html"
    queryset = Invoice.objects.all()
    paginate_by = 10
    context_object_name = "invoices"

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()
        self.filterset = InvoiceFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filterset.form
        return context


class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoices/update_invoice.html"

    def get_success_url(self) -> str:
        return reverse("detail-invoice", kwargs={"pk": self.object.pk})
