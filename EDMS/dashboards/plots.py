from types import NoneType
from typing import Dict, List, Tuple, Union

import plotly.graph_objs as go
from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from employees.models.models_salaries import Salary
from invoices.models import Invoice
from orders.models import Order

User = get_user_model()


class Plot:
    def render(self, orders: List[Order], salaries: List[Salary], text: str, is_company=False) -> str:
        plot_data = self.set_plot_data(orders=orders, salaries=salaries)
        x_data = self.set_x_values(plot_data=plot_data)
        y_data = list(plot_data.values())
        generated_date = timezone.now().strftime("%d/%m/%Y - %H:%M")
        title = f"Plot generated at {generated_date}"
        fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)])
        fig.update_layout(
            xaxis_title="Date [month/year]",
            yaxis_title="Balance [PLN]",
            title=title,
            annotations=[
                dict(
                    x=0,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text=text,
                    showarrow=False,
                )
            ],
        )
        return fig.to_html(full_html=False)

    def set_plot_data(self, orders: List[Order], salaries: List[Salary]) -> Dict[Tuple[int, int], Decimal]:
        plot_data = {}
        if len(orders) > 0 or len(salaries) > 0:
            start_month: int = orders[0].end_date.month
            start_year: int = orders[0].end_date.year
            end_month: int = timezone.now().month
            end_year: int = timezone.now().year
            month_balance = Decimal(0)
            while start_month <= end_month and start_year <= end_year:
                month_balance = self.count_month_balance(month_balance, orders, salaries, start_month, start_year)
                plot_data[(start_month, start_year)] = month_balance
                start_month, start_year = self.set_start_month_and_start_year(
                    start_month=start_month, start_year=start_year
                )
                month_balance = Decimal(0)
        return plot_data

    def count_month_balance(
        self, month_balance: Decimal, orders: List[Order], salaries: List[Salary], start_month: int, start_year: int
    ) -> Decimal:
        month_balance += self.count_month_orders_balance(orders, start_month, start_year)
        month_balance -= self.count_month_salaries_balance(salaries, start_month, start_year)
        return month_balance

    @staticmethod
    def count_month_salaries_balance(salaries: List[Salary], start_month: int, start_year: int) -> Decimal:
        month_salaries_balance = Decimal(0)
        for salary in salaries[:]:
            if salary.date.month == start_month and salary.date.year == start_year:
                month_salaries_balance += salary.fee
                salaries.remove(salary)
        return month_salaries_balance

    def count_month_orders_balance(self, orders: List[Order], start_month: int, start_year: int) -> Decimal:
        month_orders_balance = Decimal(0)
        for order in orders[:]:
            if order.end_date.month == start_month and order.end_date.year == start_year:
                month_orders_balance += self.count_single_order_balance(order=order)
                orders.remove(order)
        return month_orders_balance

    def count_single_order_balance(self, order: Order) -> Decimal:
        income_invoices = list(order.income_invoice.all())
        income_sum_net_price = self.get_sum_invoice_net_price(invoices=income_invoices)

        cost_invoices = list(order.cost_invoice.all())
        cost_sum_net_price = self.get_sum_invoice_net_price(invoices=cost_invoices)

        return income_sum_net_price - cost_sum_net_price

    @staticmethod
    def get_sum_invoice_net_price(invoices: List[Invoice]) -> Decimal:
        sum_net_price = Decimal(0)
        for invoice in invoices:
            sum_net_price += invoice.net_price
        return sum_net_price

    @staticmethod
    def set_start_month_and_start_year(start_month: int, start_year: int) -> Tuple[int, int]:
        new_month = (start_month % 12) + 1
        new_year = start_year + (start_month // 12)
        return new_month, new_year

    @staticmethod
    def set_x_values(plot_data: Dict[Tuple[int, int], Decimal]) -> List[Union[str | NoneType]]:
        x_values = []
        for month, year in plot_data.keys():
            x_values.append(f"{month}/{year}")
        return x_values


def render_plot_for_user_group(user: User) -> str:
    plot = Plot()
    text = ""
    salaries = []
    orders = []
    is_company = False
    user_group = user.groups.first()

    if user_group and user_group.name == "managers":
        text = f"Statistics employee: {user}"
        orders = list(
            Order.objects.prefetch_related("cost_invoice", "income_invoice").filter(user=user).order_by("end_date")
        )
        salaries = list(Salary.objects.filter(user=user).order_by("date"))
    elif user_group and user_group.name == "ceos":
        text = "Statistics my company"
        orders = list(Order.objects.prefetch_related("cost_invoice", "income_invoice").order_by("end_date"))
        salaries = list(Salary.objects.order_by("date"))
        is_company = True

    return plot.render(orders=orders, salaries=salaries, text=text, is_company=is_company)
