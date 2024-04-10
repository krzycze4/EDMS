from types import NoneType
from typing import Dict, List, Tuple, Union

import plotly.graph_objs as go
from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone
from employees.models.models_payment import Payment
from invoices.models import Invoice
from orders.models import Order

User = get_user_model()


class Plot:
    def render_plot(self, orders: List[Order], text: str, is_company=False) -> str:
        plot_data = self.set_plot_data(orders=orders, is_company=is_company)
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

    def set_plot_data(self, orders: List[Order], is_company: bool) -> Dict[Tuple[int, int], Decimal]:
        plot_data = {}
        if len(orders) > 0:
            start_month: int = orders[0].end_date.month
            start_year: int = orders[0].end_date.year
            end_month: int = timezone.now().month
            end_year: int = timezone.now().year

            while start_month <= end_month and start_year <= end_year:
                plot_data[(start_month, start_year)] = Decimal(0)
                for order in orders:
                    if order.end_date.month <= start_month and order.end_date.year <= start_year:
                        balance: Decimal = self.count_order_balance(order=order, is_company=is_company)
                        plot_data[(start_month, start_year)] += balance
                        orders.remove(order)
                start_month, start_year = self.set_start_month_and_year(start_month=start_month, start_year=start_year)
        return plot_data

    def count_order_balance(self, order: Order, is_company: bool) -> Decimal:
        income_invoices = order.income_invoice.all()
        income_sum_net_price = self.get_sum_invoice_net_price(invoices=income_invoices)

        cost_invoices = order.cost_invoice.all()
        cost_sum_net_price = self.get_sum_invoice_net_price(invoices=cost_invoices)

        sum_payment_fee = self.get_payment_fees(is_company=is_company, order=order)

        return income_sum_net_price - cost_sum_net_price - sum_payment_fee

    @staticmethod
    def get_sum_invoice_net_price(invoices: QuerySet[Invoice]) -> Decimal:
        sum_net_price = Decimal(0)
        for invoice in invoices:
            sum_net_price += invoice.net_price
        return sum_net_price

    @staticmethod
    def get_payment_fees(is_company, order):
        sum_payment_fee = Decimal(0)
        if is_company:
            payments = Payment.objects.filter(date__month=order.end_date.month, date__year=order.end_date.year)
        else:
            payments = Payment.objects.filter(
                date__month=order.end_date.month,
                date__year=order.end_date.year,
                user=order.user,
            )
        for payment in payments:
            sum_payment_fee += payment.fee
        return sum_payment_fee

    @staticmethod
    def set_start_month_and_year(start_month: int, start_year: int) -> Tuple[int, int]:
        new_month = (start_month % 12) + 1
        new_year = start_year + (start_month // 12)
        return new_month, new_year

    @staticmethod
    def set_x_values(plot_data: Dict[Tuple[int, int], Decimal]) -> List[Union[str | NoneType]]:
        x_values = []
        for month, year in plot_data.keys():
            x_values.append(f"{month}/{year}")
        return x_values
