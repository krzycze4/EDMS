import calendar
import secrets
from decimal import Decimal

from common_tests.consts import group_names_with_permission_codenames
from companies.factories import AddressFactory, CompanyFactory, ContactFactory
from contracts.factories import ContractFactory
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone
from employees.factories.factories_addendum import AddendumFactory
from employees.factories.factories_agreement import AgreementFactory
from employees.factories.factories_salary import SalaryFactory
from employees.factories.factories_termination import TerminationFactory
from employees.models.models_agreement import Agreement
from invoices.factories import InvoiceFactory
from orders.factories import OrderFactory, ProtocolFactory
from orders.models import Order
from users.factories import UserFactory

from EDMS.env import env
from EDMS.group_utils import create_group_with_permissions

User = get_user_model()


class Command(BaseCommand):
    help = "Generate example data in database to present how website works."
    today = timezone.now().date()
    year_ago = today - timezone.timedelta(days=365)
    month_ago = today - timezone.timedelta(days=30)
    six_months_ago = today - timezone.timedelta(days=365 // 2)
    year_ahead = today + timezone.timedelta(days=365)
    yesterday = today - timezone.timedelta(days=1)
    tomorrow = today + timezone.timedelta(days=1)

    def handle(self, *args, **options) -> None:
        """
        The main handler method that orchestrates the generation of example data by calling other methods.
        """
        self.create_users_with_groups()
        self.create_companies()
        self.create_contacts_to_companies()
        self.create_contracts()
        self.create_agreements()
        self.create_addendum()
        self.create_termination()
        self.create_salaries()
        self.create_orders_and_protocols()
        self.create_invoices()

    def create_invoices(self) -> None:
        """
        Create example invoices based on existing orders in the database.
        It generates both income and cost invoices for orders with end dates up to today.
        """
        seller = CompanyFactory.create()
        orders = Order.objects.filter(end_date__lte=self.today)
        for order in orders:
            month_ahead = order.end_date + timezone.timedelta(days=30)
            income_invoice = InvoiceFactory.create(
                seller=self.my_company,
                buyer=order.company,
                net_price=order.contract.price // Decimal(12),
                create_date=order.end_date,
                service_date=order.end_date,
                payment_date=month_ahead,
                is_paid=False if month_ahead <= self.today else True,
            )
            cost_invoices = InvoiceFactory.create_batch(
                size=3,
                seller=seller,
                buyer=self.my_company,
                net_price=Decimal(secrets.SystemRandom().uniform(1000, 25000)).quantize(Decimal("0.01")),
                create_date=order.end_date,
                service_date=order.end_date,
                payment_date=month_ahead,
            )
            order.income_invoice.add(income_invoice)
            for cost_invoice in cost_invoices:
                order.cost_invoice.add(cost_invoice)
            order.save()
        self.stdout.write(self.style.SUCCESS("Successfully generated invoices."))

    def create_orders_and_protocols(self) -> None:
        """
        Create example orders and protocols based on past, present, and future contracts.
        It generates orders for each month of the contract's duration and a corresponding protocol.
        """
        contracts = [self.past_contract, self.present_contract, self.future_contract]
        for contract in contracts:
            current_date = contract.start_date
            while current_date <= self.today:
                start_date = current_date.replace(day=1)
                last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
                end_date = current_date.replace(day=last_day_of_month)
                order = OrderFactory.create(
                    payment=contract.price // Decimal(12),
                    status=Order.CLOSED,
                    company=contract.company,
                    user=secrets.choice(contract.employee.all()),
                    contract=contract,
                    create_date=start_date,
                    start_date=start_date,
                    end_date=end_date,
                )
                ProtocolFactory.create(create_date=end_date, user=order.user, order=order)
                current_date += relativedelta(months=1)
        self.stdout.write(self.style.SUCCESS("Successfully generated orders and protocols."))

    def create_salaries(self) -> None:
        """
        Create example salaries for each agreement in the database.
        It generates a salary record for each month of the agreement's duration.
        """
        agreements = [self.agreement1, self.agreement2, self.agreement3, self.fired_manager_agreement]
        for agreement in agreements:
            current_date = agreement.start_date
            while current_date <= self.today:
                salary_date = current_date.replace(day=10)
                SalaryFactory.create(date=salary_date, user=agreement.user, fee=agreement.salary_gross)
                current_date += relativedelta(months=1)
        self.stdout.write(self.style.SUCCESS("Successfully generated salaries."))

    def create_termination(self) -> None:
        """
        Create an example termination record for the fired manager's agreement.
        """
        TerminationFactory.create(
            agreement=self.fired_manager_agreement,
            create_date=self.yesterday,
            end_date=self.yesterday,
        )
        self.stdout.write(self.style.SUCCESS("Successfully generated terminations."))

    def create_addendum(self) -> None:
        """
        Create an example addendum for the fired manager's agreement, extending its duration.
        """
        AddendumFactory.create(
            agreement=self.fired_manager_agreement,
            create_date=self.six_months_ago,
            end_date=self.year_ahead,
            salary_gross=self.fired_manager_agreement.salary_gross,
        )
        self.stdout.write(self.style.SUCCESS("Successfully generated addenda."))

    def create_agreements(self) -> None:
        """
        Create example agreements for users in the system.
        """
        self.agreement1 = AgreementFactory.create(
            create_date=self.year_ago, start_date=self.year_ago, end_date=self.year_ahead, user=self.manager1
        )
        self.agreement2 = AgreementFactory.create(
            create_date=self.year_ago,
            start_date=self.year_ago,
            end_date=self.year_ahead,
            user=self.manager2,
            type=Agreement.COMMISSION,
            salary_gross=Decimal(7000),
        )
        self.agreement3 = AgreementFactory.create(
            create_date=self.today,
            start_date=self.tomorrow,
            end_date=self.year_ahead,
            user=self.manager3,
            type=Agreement.MANDATE,
            salary_gross=Decimal(8000),
        )
        self.fired_manager_agreement = AgreementFactory.create(
            create_date=self.year_ago, start_date=self.year_ago, end_date=self.today, user=self.fired_manager
        )
        AgreementFactory.create(
            create_date=self.year_ago, start_date=self.year_ago, end_date=self.year_ahead, user=self.accountant
        )
        AgreementFactory.create(
            create_date=self.year_ago, start_date=self.year_ago, end_date=self.year_ahead, user=self.hr
        )
        AgreementFactory.create(
            create_date=self.year_ago, start_date=self.year_ago, end_date=self.year_ahead, user=self.ceo
        )
        self.stdout.write(self.style.SUCCESS("Successfully generated agreements."))

    def create_contracts(self) -> None:
        """
        Create example contracts for external companies and assign employees to them.
        """
        self.past_contract = ContractFactory.create(
            create_date=self.year_ago,
            start_date=self.year_ago,
            end_date=self.yesterday,
            company=self.external_company1,
            employee=[self.manager1, self.fired_manager],
            price=Decimal(1_000_000),
        )
        self.present_contract = ContractFactory.create(
            create_date=self.year_ago,
            start_date=self.year_ago,
            end_date=self.year_ahead,
            company=self.external_company2,
            employee=[self.manager1, self.manager2],
            price=Decimal(2_000_000),
        )
        self.future_contract = ContractFactory.create(
            create_date=self.today,
            start_date=self.tomorrow,
            end_date=self.year_ahead,
            company=self.external_company3,
            employee=[self.manager1, self.manager2, self.manager3],
            price=Decimal(3_000_000),
        )
        self.stdout.write(self.style.SUCCESS("Successfully generated contracts."))

    def create_contacts_to_companies(self) -> None:
        """
        Create example contacts for each external company.
        """
        ContactFactory.create_batch(size=10, company=self.external_company1)
        ContactFactory.create_batch(size=10, company=self.external_company2)
        ContactFactory.create_batch(size=10, company=self.external_company3)
        self.stdout.write(self.style.SUCCESS("Successfully generated contacts."))

    def create_companies(self) -> None:
        """
        Create example companies including the user's company and several external companies.
        """
        self.my_company = CompanyFactory.create(is_mine=True)
        self.external_company1 = CompanyFactory.create()
        self.external_company2 = CompanyFactory.create()
        self.external_company3 = CompanyFactory.create(address=self.external_company2.address)
        self.stdout.write(self.style.SUCCESS("Successfully generated companies."))

    def create_users_with_groups(self) -> None:
        """
        Create example users and assign them to specific groups based on predefined group names and permissions.
        """
        for group_name, permission_codenames in group_names_with_permission_codenames.items():
            create_group_with_permissions(group_name=group_name, permission_codenames=permission_codenames)
        self.accountant = self.create_user_with_group(group_name="accountants", email="accountant@example.com")
        self.ceo = self.create_user_with_group(group_name="ceos", email="ceo@example.com")
        self.hr = self.create_user_with_group(group_name="hrs", email="hr@example.com")
        self.manager1 = self.create_user_with_group(group_name="managers", email="manager1@example.com")
        self.manager2 = self.create_user_with_group(group_name="managers", email="manager2@example.com")
        self.manager3 = self.create_user_with_group(group_name="managers", email="manager3@example.com")
        self.fired_manager = self.create_user_with_group(
            group_name="managers", email="fired_manager3@example.com", is_active=False
        )
        self.stdout.write(self.style.SUCCESS("Successfully generated users."))

    @staticmethod
    def create_user_with_group(group_name: str, email: str, is_active=True) -> User:
        """
        Create a new user and assign them to a specified group.

        Args:
            group_name (str): The name of the group to which the user should be assigned.
            email (str): The email of user.
            is_active (bool): Default is_active=True. Necessary to login correctly.

        Returns:
            User: The created user who is assigned to the specified group.
        """
        group: Group = get_object_or_404(Group, name=group_name)
        password = env("EXAMPLE_PASSWORD")
        user: User = UserFactory(email=email, password=password, is_active=is_active, address=AddressFactory())
        user.groups.add(group)
        return user
