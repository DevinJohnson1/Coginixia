"""
Customer repository for data persistence
"""
from customer import Customer


class CustomerRepo:
    """Repository for managing customer data."""

    def __init__(self):
        """Initialize the repository with an empty customer store."""
        self._customers: dict[int, Customer] = {}
        self._next_id = 1

    def create(self, name: str, salary: float) -> Customer:
        """
        Create and store a new customer.

        Args:
            name: Customer's name
            salary: Customer's salary

        Returns:
            The created Customer object
        """
        customer = Customer(self._next_id, name, salary)
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

    def update(self, customer_id: int, name: str = None, salary: float = None) -> Customer | None:
        """
        Update an existing customer.

        Args:
            customer_id: The customer's ID
            name: New name (optional)
            salary: New salary (optional)

        Returns:
            The updated Customer if found, None otherwise
        """
        customer = self._customers.get(customer_id)
        if customer:
            if name is not None:
                customer.set_name(name)
            if salary is not None:
                customer.set_salary(salary)
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

