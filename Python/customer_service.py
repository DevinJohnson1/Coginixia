"""
Customer service layer for business logic
"""
from customer_repo import CustomerRepo
from models import CustomerIn, CustomerOut


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
        """
        Create a new customer.

        Args:
            customer_in: Customer input data

        Returns:
            CustomerOut model with the created customer
        """
        customer = self.repo.create(customer_in.name, customer_in.salary)
        return CustomerOut(
            id=customer.get_id(),
            name=customer.get_name(),
            salary=customer.get_salary(),
        )

    def get_customer(self, customer_id: int) -> CustomerOut | None:
        """
        Retrieve a customer by ID.

        Args:
            customer_id: The customer's ID

        Returns:
            CustomerOut model if found, None otherwise
        """
        customer = self.repo.find_by_id(customer_id)
        if customer:
            return CustomerOut(
                id=customer.get_id(),
                name=customer.get_name(),
                salary=customer.get_salary(),
            )
        return None

    def get_all_customers(self) -> list[CustomerOut]:
        """
        Retrieve all customers.

        Returns:
            List of CustomerOut models
        """
        customers = self.repo.find_all()
        return [
            CustomerOut(
                id=c.get_id(),
                name=c.get_name(),
                salary=c.get_salary(),
            )
            for c in customers
        ]

    def update_customer(
        self, customer_id: int, customer_in: CustomerIn
    ) -> CustomerOut | None:
        """
        Update an existing customer.

        Args:
            customer_id: The customer's ID
            customer_in: Updated customer data

        Returns:
            Updated CustomerOut model if found, None otherwise
        """
        customer = self.repo.update(
            customer_id, customer_in.name, customer_in.salary
        )
        if customer:
            return CustomerOut(
                id=customer.get_id(),
                name=customer.get_name(),
                salary=customer.get_salary(),
            )
        return None

    def delete_customer(self, customer_id: int) -> bool:
        """
        Delete a customer.

        Args:
            customer_id: The customer's ID

        Returns:
            True if deleted, False if not found
        """
        return self.repo.delete(customer_id)


