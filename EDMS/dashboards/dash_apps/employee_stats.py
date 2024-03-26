from typing import Dict, List, Tuple, Union

from _decimal import Decimal
from companies.models import Company
from contracts.models import Contract
from dash import Input, Output, dcc, html
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from django_plotly_dash import DjangoDash
from orders.models import Order

User = get_user_model()
app = DjangoDash("EmployeeStats")

app.layout = html.Div(
    [
        html.H4(children="Company"),
        dcc.Dropdown(id="dropdown-company", multi=True),
        html.Div(id="dummy-input", style={"display": "none"}),
        html.H4(children="Contract"),
        dcc.Dropdown(id="dropdown-contract", multi=True),
        dcc.Graph(id="graph-balance"),
    ]
)


@app.callback(
    [Output("dropdown-company", "options"), Output("dropdown-company", "value")],
    Input("dummy-input", "children"),
)
def update_company_dropdown(dummy_input, user: User):
    employee_companies = Company.objects.filter(contracts__employee=user).distinct()
    options = [
        {"label": company.name, "value": company.name} for company in employee_companies
    ]
    values = options
    return options, values


@app.callback(
    [Output("dropdown-contract", "options"), Output("dropdown-contract", "value")],
    Input("dropdown-company", "value"),
)
def update_contract_dropdown(selected_companies: List[Dict[str, str]], user: User):
    selected_company_names = get_names(selected_objects=selected_companies)
    employee_contracts = Contract.objects.filter(
        company__name__in=selected_company_names, employee__exact=user
    ).distinct()
    options = [
        {"label": contract.name, "value": contract.name}
        for contract in employee_contracts
    ]
    values = options
    return options, values


@app.callback(Output("graph-balance", "figure"), Input("dropdown-contract", "value"))
def update_graph_balance(selected_contracts: List[Dict[str, str]], user: User):
    graph_data = {}
    figure = {
        "layout": {
            "title": "Your balance",
            "xaxis": {
                "title": "Date",
            },
            "yaxis": {"title": "Balance"},
        }
    }
    selected_contract_names = get_names(selected_objects=selected_contracts)
    connected_orders = (
        Order.objects.filter(contract__name__in=selected_contract_names, user=user)
        .distinct()
        .order_by("end_date")
    )
    if selected_contract_names and connected_orders.exists():
        start_month = connected_orders.first().end_date.month
        start_year = connected_orders.first().end_date.year
        end_month = timezone.now().month
        end_year = timezone.now().year

        while start_month <= end_month and start_year <= end_year:
            figure["data"] = set_figure_data(
                connected_orders=connected_orders,
                graph_data=graph_data,
                start_month=start_month,
                start_year=start_year,
            )
            start_month, start_year = set_start_month_and_year(
                start_month=start_month, start_year=start_year
            )
    return figure


def set_figure_data(
    connected_orders: QuerySet[Order],
    graph_data: Dict[Tuple[int, int], Decimal],
    start_month: int,
    start_year: int,
    graph_type="bar",
) -> List[Dict[str, List[Union[str | Decimal]]]]:
    graph_data[(start_month, start_year)] = count_balance(
        connected_orders=connected_orders,
        start_month=start_month,
        start_year=start_year,
    )
    x_values = set_x_values(graph_data)
    return [{"x": x_values, "y": list(graph_data.values()), "type": graph_type}]


def set_x_values(graph_data: Dict[Tuple[int, int], Decimal]) -> List[str]:
    x_values = []
    for x_value in graph_data.keys():
        x_values.append(f"{x_value[0]}/{x_value[1]}")
    return x_values


def count_balance(
    connected_orders: QuerySet[Order], start_month: int, start_year: int
) -> Decimal:
    orders = connected_orders.filter(
        end_date__month=start_month, end_date__year=start_year
    )
    balance = Decimal(0)
    for order in orders:
        for income_invoice in order.income_invoice.all():
            balance += income_invoice.net_price
        for cost_invoice in order.cost_invoice.all():
            balance -= cost_invoice.net_price
    return balance


def get_names(selected_objects: List[Union[Dict[str, str] | str]]) -> List[str]:
    names = []
    if len(selected_objects) > 0 and isinstance(selected_objects[0], dict):
        for company_dict in selected_objects:
            names.append(company_dict["label"])
    elif len(selected_objects) > 0 and isinstance(selected_objects[0], str):
        names = selected_objects
    return names


def set_start_month_and_year(start_month: int, start_year: int) -> Tuple[int, int]:
    if start_month < 12:
        start_month += 1
    else:
        start_month = 1
        start_year += 1
    return start_month, start_year
