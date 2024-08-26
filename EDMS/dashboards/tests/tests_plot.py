from decimal import Decimal

from companies.factories import CompanyFactory
from dashboards.plots import Plot, render_plot_for_user_group
from django.test import TestCase
from django.utils import timezone
from employees.factories.factories_salary import SalaryFactory
from invoices.factories import InvoiceFactory
from orders.factories import OrderFactory
from users.factories import UserFactory

from EDMS.group_utils import create_group_with_permissions


class PlotTest(TestCase):
    def setUp(self) -> None:
        self.plot = Plot()
        self.user = UserFactory.create()
        self.my_company = CompanyFactory.create(is_mine=True)
        self.order = OrderFactory.create(user=self.user)
        self.salary = SalaryFactory.create(user=self.user)
        self.text = "Test"
        self.income_invoice = InvoiceFactory.create(seller=self.my_company, buyer=self.order.company)
        self.cost_invoice = InvoiceFactory.create(buyer=self.my_company, seller=self.order.company)

    def test_render_method_return_string(self):
        result = self.plot.render(orders=[self.order], salaries=[self.salary], text=self.text)
        self.assertTrue(isinstance(result, str))

    def test_set_plot_data_when_orders_is_empty_and_salaries_is_empty(self):
        result = self.plot.set_plot_data(orders=[], salaries=[])
        self.assertEqual(result, {})

    def test_set_plot_data_when_orders_is_empty_and_salaries_not_empty(self):
        result = self.plot.set_plot_data(orders=[], salaries=[self.salary])
        self.assertNotEquals(result, {})

    def test_set_plot_data_when_orders_not_empty_and_salaries_is_empty_and_order_end_date_not_future_month(self):
        self.order.income_invoice.add(self.income_invoice)
        self.order.cost_invoice.add(self.cost_invoice)
        create_date = timezone.now().date() - timezone.timedelta(days=60)
        start_date = timezone.now().date() - timezone.timedelta(days=60)
        end_date = timezone.now().date() - timezone.timedelta(days=32)
        self.order.create_date = create_date
        self.order.start_date = start_date
        self.order.end_date = end_date
        self.order.save()
        self.order.refresh_from_db()
        result = self.plot.set_plot_data(orders=[self.order], salaries=[])
        self.assertNotEquals(result, {})

    def test_set_plot_data_when_orders_not_empty_and_salaries_is_empty_and_order_end_date_is_future_month(self):
        self.order.income_invoice.add(self.income_invoice)
        self.order.cost_invoice.add(self.cost_invoice)
        self.order.refresh_from_db()
        result = self.plot.set_plot_data(orders=[self.order], salaries=[])
        self.assertEqual(result, {})

    def test_set_start_date_when_orders_and_salaries_not_exist(self):
        result = self.plot.set_start_date(orders=[], salaries=[])
        expected_value = (None, None)
        self.assertEqual(result, expected_value)

    def test_set_start_date_when_orders_exist_and_salaries_not_exist(self):
        result = self.plot.set_start_date(orders=[self.order], salaries=[])
        expected_value = (self.order.end_date.month, self.order.end_date.year)
        self.assertEqual(result, expected_value)

    def test_set_start_date_when_orders_not_exist_and_salaries_exist(self):
        result = self.plot.set_start_date(orders=[], salaries=[self.salary])
        expected_value = (self.salary.date.month, self.salary.date.year)
        self.assertEqual(result, expected_value)

    def test_set_start_date_when_orders_end_date_before_salaries_date(self):
        create_date_order = timezone.now().date() - timezone.timedelta(days=200)
        start_date_order = timezone.now().date() - timezone.timedelta(days=200)
        end_date_order = timezone.now().date() - timezone.timedelta(days=100)
        self.order.create_date = create_date_order
        self.order.start_date = start_date_order
        self.order.end_date = end_date_order
        self.order.save()
        self.order.refresh_from_db()
        date_salary = timezone.now().date() - timezone.timedelta(days=60)
        self.salary.date = date_salary
        self.salary.save()
        self.salary.refresh_from_db()
        result = self.plot.set_start_date(orders=[self.order], salaries=[self.salary])
        expected_value = (self.order.end_date.month, self.order.end_date.year)
        self.assertEqual(result, expected_value)

    def test_set_start_date_when_orders_end_date_after_salaries_date(self):
        create_date_order = timezone.now().date() - timezone.timedelta(days=200)
        start_date_order = timezone.now().date() - timezone.timedelta(days=200)
        end_date_order = timezone.now().date() - timezone.timedelta(days=100)
        self.order.create_date = create_date_order
        self.order.start_date = start_date_order
        self.order.end_date = end_date_order
        self.order.save()
        self.order.refresh_from_db()
        date_salary = timezone.now().date() - timezone.timedelta(days=150)
        self.salary.date = date_salary
        self.salary.save()
        self.salary.refresh_from_db()
        result = self.plot.set_start_date(orders=[self.order], salaries=[self.salary])
        expected_value = (self.salary.date.month, self.salary.date.year)
        self.assertEqual(result, expected_value)

    def test_count_month_balance_when_orders_not_exist_and_salaries_not_exist(self):
        month_balance = Decimal(0)
        result = self.plot.count_month_balance(
            month_balance=month_balance, orders=[], salaries=[], start_month=0, start_year=0
        )
        self.assertEqual(result, month_balance)

    def test_count_month_balance_when_orders_exist_and_salaries_not_exist(self):
        create_date_order = timezone.now().date() - timezone.timedelta(days=200)
        start_date_order = timezone.now().date() - timezone.timedelta(days=200)
        end_date_order = timezone.now().date() - timezone.timedelta(days=100)
        self.order.create_date = create_date_order
        self.order.start_date = start_date_order
        self.order.end_date = end_date_order
        self.order.income_invoice.add(self.income_invoice)
        self.order.save()
        self.order.refresh_from_db()
        start_month = self.order.end_date.month
        start_year = self.order.end_date.year
        expected_value = self.plot.count_month_orders_balance(
            orders=[self.order], start_month=start_month, start_year=start_year
        )
        month_balance = Decimal(0)
        result = self.plot.count_month_balance(
            month_balance=month_balance,
            orders=[self.order],
            salaries=[],
            start_month=start_month,
            start_year=start_year,
        )
        self.assertEqual(result, expected_value)

    def test_count_month_balance_when_orders_not_exist_and_salaries_exist(self):
        date_salary = timezone.now().date() - timezone.timedelta(days=150)
        self.salary.date = date_salary
        self.order.income_invoice.add(self.income_invoice)
        self.order.save()
        self.order.refresh_from_db()
        start_month = self.salary.date.month
        start_year = self.salary.date.year
        expected_value = self.plot.count_month_salaries_balance(
            salaries=[self.salary], start_month=start_month, start_year=start_year
        )
        month_balance = Decimal(0)
        result = self.plot.count_month_balance(
            month_balance=month_balance,
            orders=[],
            salaries=[self.salary],
            start_month=start_month,
            start_year=start_year,
        )
        self.assertEqual(result, -expected_value)

    def test_count_single_order_balance_method(self):
        self.order.income_invoice.add(self.income_invoice)
        self.order.cost_invoice.add(self.cost_invoice)
        self.order.save()
        self.order.refresh_from_db()
        result = self.plot.count_single_order_balance(order=self.order)
        expected_value = self.income_invoice.net_price - self.cost_invoice.net_price
        self.assertEqual(result, expected_value)

    def test_get_sum_invoice_net_price_method_when_invoice_not_exist(self):
        result = self.plot.get_sum_invoice_net_price(invoices=[])
        expected_value = Decimal(0)
        self.assertEqual(result, expected_value)

    def test_get_sum_invoice_net_price_method_when_invoice_exists(self):
        result = self.plot.get_sum_invoice_net_price(invoices=[self.income_invoice])
        expected_value = self.income_invoice.net_price
        self.assertEqual(result, expected_value)

    def test_set_start_month_and_start_year(self):
        result = self.plot.set_start_month_and_start_year(start_month=12, start_year=2024)
        expected_value = (1, 2025)
        self.assertEqual(result, expected_value)

    def test_x_values_method_when_plot_data_is_empty(self):
        result = self.plot.set_x_values(plot_data={})
        self.assertEqual(result, [])

    def test_x_values_method_when_plot_data_not_empty(self):
        create_date_order = timezone.now().date() - timezone.timedelta(days=200)
        start_date_order = timezone.now().date() - timezone.timedelta(days=200)
        end_date_order = timezone.now().date() - timezone.timedelta(days=31)
        self.order.create_date = create_date_order
        self.order.start_date = start_date_order
        self.order.end_date = end_date_order
        self.order.income_invoice.add(self.income_invoice)
        self.order.save()
        self.order.refresh_from_db()
        plot_data = self.plot.set_plot_data(orders=[self.order], salaries=[])
        result = self.plot.set_x_values(plot_data=plot_data)
        expected_value = [
            f"{self.order.end_date.month}/{self.order.end_date.year}",
            f"{timezone.now().month}/{timezone.now().year}",
        ]
        self.assertEqual(result, expected_value)

    def test_redner_plot_for_user_group_managers(self):
        manager = UserFactory.create()
        managers_group = create_group_with_permissions(group_name="managers", permission_codenames=[])
        manager.groups.add(managers_group)
        manager.save()
        manager.refresh_from_db()
        expected_text = f"Statistics employee: {manager}"
        result = render_plot_for_user_group(manager)
        self.assertIn(expected_text, result)

    def test_redner_plot_for_user_group_ceos(self):
        ceo = UserFactory.create()
        ceos_group = create_group_with_permissions(group_name="ceos", permission_codenames=[])
        ceo.groups.add(ceos_group)
        ceo.save()
        ceo.refresh_from_db()
        expected_text = "Statistics my company"
        result = render_plot_for_user_group(ceo)
        self.assertIn(expected_text, result)
