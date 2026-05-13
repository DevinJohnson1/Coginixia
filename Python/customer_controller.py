"""
Customer controller with FastAPI routes
"""
from fastapi import APIRouter, HTTPException
from models import CustomerIn, CustomerOut
from customer_service import CustomerService

# Create a router for customer endpoints
router = APIRouter(prefix="/api/customers", tags=["customers"])


class CustomerController:
    """Controller for handling customer API requests."""

    def __init__(self, service: CustomerService):
        """
        Initialize the controller with a service.

        Args:
            service: CustomerService instance
        """
        self.service = service
        self._setup_routes()

    def _setup_routes(self):
        """Setup all customer routes."""
        router.post("", response_model=CustomerOut, status_code=201)(self.create_customer)
        router.get("", response_model=list[CustomerOut])(self.get_all_customers)
        router.get("/salary/min/{customer_salary}", response_model=list[CustomerOut])(self.get_salary_minimum)
        router.get("/{customer_id}", response_model=CustomerOut)(self.get_customer)
        router.put("/{customer_id}", response_model=CustomerOut)(self.update_customer)
        router.delete("/{customer_id}", status_code=204)(self.delete_customer)

    # POST
    # endpoint: /api/customers
    # Full URL: http://localhost:8000/api/customers OR "BaseURL/api/customers"
    # Returns: CustomerOut (single customer object with id, name, salary)
    async def create_customer(self, customer_in: CustomerIn) -> CustomerOut:
        """
        Create a new customer.

        Args:
            customer_in: Customer input data

        Returns:
            Created customer
        """
        return self.service.create_customer(customer_in)

    # GET
    # endpoint: /api/customers/min/salary/n
    # Full URL: http://localhost:8000/api/customers/min/salary/n OR "BaseURL/api/customers/min/salary/n"
    # Returns: list[CustomerOut] (array of customer objects) with minimum salary threshold n.
    async def get_salary_minimum(self, customer_salary: float) -> list[CustomerOut]:
        """
        Get all customers with a specified minimum salary or higher.

        Args:
            customer_salary: The minimum salary threshold

        Returns:
            List of all customers with a salary equal to or higher than the threshold.

        Raises:
            HTTPException: If no customers found with specified minimum salary or higher
        """
        customers = self.service.get_salary_minimum(customer_salary)
        if not customers:
            raise HTTPException(
                status_code=404,
                detail=f"No customers found with minimum salary of {customer_salary} or higher",
            )
        return customers


    # GET
    # endpoint: /api/customers
    # Full URL: http://localhost:8000/api/customers OR "BaseURL/api/customers"
    # Returns: list[CustomerOut] (array of customer objects)
    async def get_all_customers(self) -> list[CustomerOut]:
        """
        Get all customers.

        Returns:
            List of all customers
        """
        return self.service.get_all_customers()

    # GET
    # endpoint: /api/customers/{customer_id}
    # Full URL: http://localhost:8000/api/customers/{id} OR "BaseURL/api/customers/{id}"
    # Returns: CustomerOut (single customer object with id, name, salary)
    async def get_customer(self, customer_id: int) -> CustomerOut:
        """
        Get a customer by ID.

        Args:
            customer_id: The customer's ID

        Returns:
            The requested customer

        Raises:
            HTTPException: If customer not found
        """
        customer = self.service.get_customer(customer_id)
        if not customer:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )
        return customer

    # PUT
    # endpoint: /api/customers/{customer_id}
    # Full URL: http://localhost:8000/api/customers/{id} OR "BaseURL/api/customers/{id}"
    # Returns: CustomerOut (updated customer object with id, name, salary)
    async def update_customer(
        self, customer_id: int, customer_in: CustomerIn
    ) -> CustomerOut:
        """
        Update an existing customer.

        Args:
            customer_id: The customer's ID
            customer_in: Updated customer data

        Returns:
            Updated customer

        Raises:
            HTTPException: If customer not found
        """
        customer = self.service.update_customer(customer_id, customer_in)
        if not customer:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )
        return customer

    # DELETE
    # endpoint: /api/customers/{customer_id}
    # Full URL: http://localhost:8000/api/customers/{id} OR "BaseURL/api/customers/{id}"
    # Returns: None (HTTP 204 No Content on success)
    async def delete_customer(self, customer_id: int) -> None:
        """
        Delete a customer.

        Args:
            customer_id: The customer's ID

        Raises:
            HTTPException: If customer not found
        """
        success = self.service.delete_customer(customer_id)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )








