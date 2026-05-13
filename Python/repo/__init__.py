"""
Repository layer for data persistence
"""
from domain.customer import Customer
from domain.account import Account


class CustomerRepo:
    """Repository for managing customer data."""

    def __init__(self):
        """Initialize the repository with an empty customer store."""
        self._customers: dict[int, Customer] = {}
        self._next_id = 1

    def create(self, name: str, account: Account) -> Customer:
        """
        Create and store a new customer.

        Args:
            name: Customer's name
            account: Customer's account

        Returns:
            The created Customer object
        """
        customer = Customer(self._next_id, name, account)
        self._customers[self._next_id] = customer
        self._next_id += 1
        return customer

    def find_by_id(self, customer_id: int) -> Customer | None:
        """
        Find a customer by their ID.

        Args:
            customer_id: The customer's ID

        Returns:
            The Customer if found, None otherwise
        """
        return self._customers.get(customer_id)

    def find_all(self) -> list[Customer]:
        """
        Get all customers.

        Returns:
            A list of all Customer objects
        """
        return list(self._customers.values())

    def find_balance_minimum(self, balance: float) -> list[Customer]:
        """
        Get all customers with specified or more account balance.

        Returns:
            A list of all Customer objects with account balances higher than or equal to the specified value.
        """
        return [customer for customer in self._customers.values() if customer.get_account().get_balance() >= balance]

    def update(self, customer_id: int, name: str = None, account: Account = None) -> Customer | None:
        """
        Update an existing customer.

        Args:
            customer_id: The customer's ID
            name: New name (optional)
            account: New account (optional)

        Returns:
            The updated Customer if found, None otherwise
        """
        customer = self._customers.get(customer_id)
        if customer:
            if name is not None:
                customer.set_name(name)
            if account is not None:
                customer.set_account(account)
        return customer

    def delete(self, customer_id: int) -> bool:
        """
        Delete a customer.

        Args:
            customer_id: The customer's ID

        Returns:
            True if deleted, False if not found
        """
        if customer_id in self._customers:
            del self._customers[customer_id]
            return True
        return False

