"""
Customer controller with FastAPI routes
"""
from fastapi import APIRouter, Depends, HTTPException
from utilities.auth import require_path_secret
from models import CustomerIn, CustomerOut
from services import CustomerService

# Create a router for customer endpoints
router = APIRouter(
    prefix="/api/{api_secret}/customers",
    tags=["customers"],
    dependencies=[Depends(require_path_secret)],
)


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
        router.get("/premium", response_model=list[CustomerOut])(self.get_premium)
        router.get("/balance/min/{balance}", response_model=list[CustomerOut])(self.get_balance_minimum)
        router.get("/{customer_id}", response_model=CustomerOut)(self.get_customer)
        router.put("/{customer_id}", response_model=CustomerOut)(self.update_customer)
        router.delete("/{customer_id}", status_code=204)(self.delete_customer)

    # POST
    # endpoint: /api/customers
    # Full URL: http://localhost:8000/api/customers OR "BaseURL/api/customers"
    # Returns: CustomerOut (single customer object with id, name, account)
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
    # endpoint: /api/customers/balance/min/n
    # Full URL: http://localhost:8000/api/customers/balance/min/n OR "BaseURL/api/customers/balance/min/n"
    # Returns: list[CustomerOut] (array of customer objects) with minimum account balance of n.
    async def get_balance_minimum(self, balance: float) -> list[CustomerOut]:
        """
        Get all customers with a specified minimum account balance or higher.

        Args:
            balance: The minimum balance threshold

        Returns:
            List of all customers with an account balance equal to or higher than the threshold.

        Raises:
            HTTPException: If no customers found with specified minimum balance or higher
        """
        customers = self.service.get_salary_minimum(balance)
        if not customers:
            raise HTTPException(
                status_code=404,
                detail=f"No customers found with minimum account balance of ${balance} or higher",
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
    # endpoint: /api/customers/premium
    # Full URL: http://localhost:8000/api/customers/premium OR "BaseURL/api/customers/premium"
    # Returns: list[CustomerOut] (array of premium customer objects with balance > 10000)
    async def get_premium(self) -> list[CustomerOut]:
        """
        Get all premium customers with account balance greater than 10000.

        Returns:
            List of all premium customers

        Raises:
            HTTPException: If no premium customers found
        """
        customers = self.service.get_premium()
        if not customers:
            raise HTTPException(
                status_code=404,
                detail="No premium customers found with account balance greater than $10,000",
            )
        return customers

    # GET
    # endpoint: /api/customers/{customer_id}
    # Full URL: http://localhost:8000/api/customers/{id} OR "BaseURL/api/customers/{id}"
    # Returns: CustomerOut (single customer object with id, name, account)
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
    # Returns: CustomerOut (updated customer object with id, name, account)
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

