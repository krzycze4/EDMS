from django.shortcuts import render
from django.views.generic import TemplateView


def test_view(request):
    return render(request=request, template_name="dashboards/dashboard.html")


# class DashboardView(TemplateView):
#     template_name = 'dashboards/dashboard.html'
