from typing import Dict, List, Union

from companies.models import Company
from contracts.models import Contract
from dash import Input, Output, dcc, html
from dashboards.dash_apps.employee_stats import (
    set_figure_data,
    set_start_month_and_year,
)
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_plotly_dash import DjangoDash
from orders.models import Order

User = get_user_model()
app_company = DjangoDash("CompanyStats")

app_company.layout = html.Div(
    [
        html.H4(children="Companies"),
        dcc.Dropdown(id="dropdown-company", multi=True),
        html.Div(id="dummy-input", style={"display": "none"}),
        html.H4(children="Employees"),
        dcc.Dropdown(id="dropdown-employee", multi=True),
        html.H4(children="Contracts"),
        dcc.Dropdown(id="dropdown-contract", multi=True),
        dcc.Graph(id="graph-balance"),
    ]
)


@app_company.callback(
    [Output("dropdown-company", "options"), Output("dropdown-company", "value")],
    Input("dummy-input", "children"),
)
def update_company_dropdown(dummy_input):
    companies = Company.objects.filter(contracts__isnull=False).distinct()
    options = [{"label": company.name, "value": company.id} for company in companies]
    values = options
    return options, values


@app_company.callback(
    [Output("dropdown-employee", "options"), Output("dropdown-employee", "value")],
    Input("dropdown-company", "value"),
)
def update_users_dropdown(selected_companies: List[Union[Dict[str, int]] | int]):
    company_ids = get_ids(selected_objects=selected_companies)
    contracts = Contract.objects.filter(company__id__in=company_ids).distinct()
    employees = User.objects.filter(contracts__in=contracts).distinct()
    options = [
        {"label": f"{employee.first_name} {employee.last_name}", "value": employee.id}
        for employee in employees
    ]
    values = options
    return options, values


@app_company.callback(
    [Output("dropdown-contract", "options"), Output("dropdown-contract", "value")],
    Input("dropdown-employee", "value"),
)
def update_contract_dropdown(
    selected_employees: List[Union[Dict[str, Union[str | int]]] | int]
):
    employee_ids = get_ids(selected_objects=selected_employees)
    contracts = Contract.objects.filter(employee__id__in=employee_ids).distinct()
    options = [{"label": contract.name, "value": contract.id} for contract in contracts]
    values = options
    return options, values


def get_ids(selected_objects: List[Union[Dict[str, int]] | int]) -> List[int]:
    object_ids = []
    if len(selected_objects) > 0 and isinstance(selected_objects[0], int):
        object_ids = selected_objects
    else:
        for company_dict in selected_objects:
            object_ids.append(company_dict["value"])
    return object_ids


@app_company.callback(
    Output("graph-balance", "figure"), Input("dropdown-contract", "value")
)
def update_graph_balance(selected_contracts: List[Union[Dict[str, int]] | int]):
    graph_data = {}

    contract_ids = get_ids(selected_objects=selected_contracts)
    orders = (
        Order.objects.filter(contract__id__in=contract_ids)
        .distinct()
        .order_by("end_date")
    )
    figure = {
        "layout": {
            "title": "Your company balance",
            "xaxis": {
                "title": "Date",
            },
            "yaxis": {"title": "Balance"},
        }
    }
    if contract_ids and orders.exists():
        start_month = orders.first().end_date.month
        start_year = orders.first().end_date.year
        end_month = timezone.now().month
        end_year = timezone.now().year

        while start_month <= end_month and start_year <= end_year:
            figure["data"] = set_figure_data(
                connected_orders=orders,
                graph_data=graph_data,
                start_month=start_month,
                start_year=start_year,
            )
            start_month, start_year = set_start_month_and_year(
                start_month=start_month, start_year=start_year
            )
    return figure
