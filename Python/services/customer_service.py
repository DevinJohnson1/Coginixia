"""Business logic for customer management."""
from __future__ import annotations
from typing import Optional

from repo.customer_repo import CustomerRepo
from domain.account import Account
from models import CustomerIn, CustomerOut, AccountOut


class CustomerService:
    """Service layer for customer business logic."""

    def __init__(self, repo: CustomerRepo):
        """
        Initialize the service with a repository.

        Args:
            repo: CustomerRepo instance for data access
        """
        self.repo = repo

    def create_customer(self, customer_in: CustomerIn) -> CustomerOut:
        """Create a new customer."""
        account = Account(
            id=0,  # Temporary ID, will be set by persistence layer
            account_type=customer_in.account.account_type,
            balance=customer_in.account.balance,
        )
        customer = self.repo.create(customer_in.name, account)
        return self._customer_to_out(customer)

    def get_customer(self, customer_id: int) -> Optional[CustomerOut]:
        """Retrieve a customer by ID."""
        customer = self.repo.find_by_id(customer_id)
        if customer:
            return self._customer_to_out(customer)
        return None

    def get_all_customers(self) -> list[CustomerOut]:
        """Retrieve all customers."""
        customers = self.repo.find_all()
        return [self._customer_to_out(c) for c in customers]

    def get_salary_minimum(self, balance: float) -> list[CustomerOut]:
        """Retrieve all customers with a minimum specified account balance or higher."""
        customers = self.repo.find_balance_minimum(balance)
        return [self._customer_to_out(c) for c in customers]

    def get_premium(self) -> list[CustomerOut]:
        """Retrieve all premium customers (account balance > 10000)."""
        customers = self.repo.get_premium()
        return [self._customer_to_out(c) for c in customers]

    def update_customer(
        self, customer_id: int, customer_in: CustomerIn
    ) -> Optional[CustomerOut]:
        """Update an existing customer."""
        account = Account(
            id=0,  # Temporary ID
            account_type=customer_in.account.account_type,
            balance=customer_in.account.balance,
        )
        customer = self.repo.update(customer_id, customer_in.name, account)
        if customer:
            return self._customer_to_out(customer)
        return None

    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer."""
        return self.repo.delete(customer_id)

    def _customer_to_out(self, customer) -> CustomerOut:
        """Convert a Customer domain object to CustomerOut model."""
        account = customer.get_account()
        return CustomerOut(
            id=customer.get_id(),
            name=customer.get_name(),
            account=AccountOut(
                id=account.get_id(),
                account_type=account.get_account_type(),
                balance=account.get_balance(),
            ),
        )

