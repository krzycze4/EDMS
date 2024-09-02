from decimal import Decimal
from types import NoneType
from typing import Dict, List, Tuple, Union

import plotly.graph_objs as go
from django.contrib.auth import get_user_model
from django.utils import timezone
from employees.models.models_salaries import Salary
from invoices.models import Invoice
from orders.models import Order

User = get_user_model()


class Plot:
    def render(self, orders: List[Order], salaries: List[Salary], text: str, is_company=False) -> str:
        """
        Create a plot based on the given orders and salaries.

        Args:
            orders (List[Order]): List of order objects.
            salaries (List[Salary]): List of salary objects.
            text (str): Text to display on the plot.
            is_company (bool): Flag to indicate if the plot is for a company.

        Returns:
            str: HTML string of the plot.
        """
        plot_data = self.set_plot_data(orders=orders, salaries=salaries)
        print(plot_data)
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
        """
        Prepare data for the plot based on orders and salaries.

        Args:
            orders (List[Order]): List of order objects.
            salaries (List[Salary]): List of salary objects.

        Returns:
            Dict[Tuple[int, int], Decimal]: Data for the plot, with month/year as keys and balance as values.
        """
        plot_data = {}
        if not orders and not salaries:
            return plot_data
        month = 0
        year = 1
        start_date = self.set_start_date(orders=orders, salaries=salaries)
        start_month: int = start_date[month]
        start_year: int = start_date[year]
        end_month: int = timezone.now().month
        end_year: int = timezone.now().year
        month_balance = Decimal(0)
        while timezone.datetime(day=1, month=start_month, year=start_year) <= timezone.datetime(
            day=1, month=end_month, year=end_year
        ):
            month_balance = self.count_month_balance(month_balance, orders, salaries, start_month, start_year)
            plot_data[(start_month, start_year)] = month_balance
            start_month, start_year = self.set_start_month_and_start_year(
                start_month=start_month, start_year=start_year
            )
            month_balance = Decimal(0)
        return plot_data

    @staticmethod
    def set_start_date(orders: List[Order], salaries: List[Salary]) -> Tuple[int, int]:
        """
        Set the start month and year for plotting.

        Args:
            orders (List[Order]): List of order objects.
            salaries (List[Salary]): List of salary objects.

        Returns:
            Tuple[int, int]: Start month and year.
        """
        start_month, start_year = None, None

        if orders:
            first_order_date = min(order.end_date for order in orders)
            start_month = first_order_date.month
            start_year = first_order_date.year

        if salaries:
            first_salary_date = min(salary.date for salary in salaries)
            salary_month = first_salary_date.month
            salary_year = first_salary_date.year

            if (
                start_month is None
                or (salary_year < start_year)
                or (salary_year == start_year and salary_month < start_month)
            ):
                start_month = salary_month
                start_year = salary_year
        return start_month, start_year

    def count_month_balance(
        self, month_balance: Decimal, orders: List[Order], salaries: List[Salary], start_month: int, start_year: int
    ) -> Decimal:
        """
        Calculate the money balance for a specific month.

        Args:
            month_balance (Decimal): Current money month balance.
            orders (List[Order]): List of order objects.
            salaries (List[Salary]): List of salary objects.
            start_month (int): Month to calculate the balance for.
            start_year (int): Year to calculate the balance for.

        Returns:
            Decimal: Money balance for the month.
        """
        month_balance += self.count_month_orders_balance(orders, start_month, start_year)
        month_balance -= self.count_month_salaries_balance(salaries, start_month, start_year)
        return month_balance

    @staticmethod
    def count_month_salaries_balance(salaries: List[Salary], start_month: int, start_year: int) -> Decimal:
        """
        Calculate total salaries money for a specific month.

        Args:
            salaries (List[Salary]): List of salary objects.
            start_month (int): Month to calculate the salaries for.
            start_year (int): Year to calculate the salaries for.

        Returns:
            Decimal: Total salaries money for the month.
        """
        month_salaries_balance = Decimal(0)
        for salary in salaries[:]:
            if salary.date.month == start_month and salary.date.year == start_year:
                month_salaries_balance += salary.fee
                salaries.remove(salary)
        return month_salaries_balance

    def count_month_orders_balance(self, orders: List[Order], start_month: int, start_year: int) -> Decimal:
        """
        Calculate total order balance money for a specific month.

        Args:
            orders (List[Order]): List of order objects.
            start_month (int): Month to calculate the order income for.
            start_year (int): Year to calculate the order income for.

        Returns:
            Decimal: Total order money balance for the month.
        """
        month_orders_balance = Decimal(0)
        for order in orders[:]:
            if order.end_date.month == start_month and order.end_date.year == start_year:
                month_orders_balance += self.count_single_order_balance(order=order)
                orders.remove(order)
        return month_orders_balance

    def count_single_order_balance(self, order: Order) -> Decimal:
        """
        Calculate the balance money for a single order.

        Args:
            order (Order): Order object.

        Returns:
            Decimal: Money balance for the order.
        """
        income_invoices = list(order.income_invoice.all())
        income_sum_net_price = self.get_sum_invoice_net_price(invoices=income_invoices)

        cost_invoices = list(order.cost_invoice.all())
        cost_sum_net_price = self.get_sum_invoice_net_price(invoices=cost_invoices)

        return income_sum_net_price - cost_sum_net_price

    @staticmethod
    def get_sum_invoice_net_price(invoices: List[Invoice]) -> Decimal:
        """
        Calculate the total net price of invoices.

        Args:
            invoices (List[Invoice]): List of invoice objects.

        Returns:
            Decimal: Total net price of invoices.
        """
        sum_net_price = Decimal(0)
        for invoice in invoices:
            sum_net_price += invoice.net_price
        return sum_net_price

    @staticmethod
    def set_start_month_and_start_year(start_month: int, start_year: int) -> Tuple[int, int]:
        """
        Set the next month and year from the given month and year.

        Args:
            start_month (int): Current month.
            start_year (int): Current year.

        Returns:
            Tuple[int, int]: Next month and year.
        """
        new_month = (start_month % 12) + 1
        new_year = start_year + (start_month // 12)
        return new_month, new_year

    @staticmethod
    def set_x_values(plot_data: Dict[Tuple[int, int], Decimal]) -> List[Union[str | NoneType]]:
        """
        Get the x-axis labels for the plot.

        Args:
            plot_data (Dict[Tuple[int, int], Decimal]): Data used to generate the plot.

        Returns:
            List[Union[str | NoneType]]: List of x-axis labels.
        """
        x_values = []
        for month, year in plot_data.keys():
            x_values.append(f"{month}/{year}")
        return x_values


def render_plot_for_user_group(user: User) -> str:
    """
    Generate a plot based on the user's group.

    Args:
        user (User): User object.

    Returns:
        str: HTML string of the plot.
    """
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
