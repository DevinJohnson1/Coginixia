"""Customer controller with FastAPI routes."""
from fastapi import APIRouter, HTTPException

from models import CustomerIn, CustomerOut
from services.customer_service import CustomerService

# Router for customer endpoints
router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
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
        router.get("/balance/min/{balance}", response_model=list[CustomerOut])(
            self.get_balance_minimum
        )
        router.get("/{customer_id}", response_model=CustomerOut)(self.get_customer)
        router.put("/{customer_id}", response_model=CustomerOut)(self.update_customer)
        router.delete("/{customer_id}", status_code=204)(self.delete_customer)

    # POST /api/customers
    async def create_customer(self, customer_in: CustomerIn) -> CustomerOut:
        """Create a new customer."""
        return self.service.create_customer(customer_in)

    # GET /api/customers/balance/min/{balance}
    async def get_balance_minimum(self, balance: float) -> list[CustomerOut]:
        """Get all customers with a specified minimum account balance or higher."""
        customers = self.service.get_salary_minimum(balance)
        if not customers:
            raise HTTPException(
                status_code=404,
                detail=f"No customers found with minimum account balance of ${balance} or higher",
            )
        return customers

    # GET /api/customers
    async def get_all_customers(self) -> list[CustomerOut]:
        """Get all customers."""
        return self.service.get_all_customers()

    # GET /api/customers/premium
    async def get_premium(self) -> list[CustomerOut]:
        """Get all premium customers with account balance greater than 10000."""
        customers = self.service.get_premium()
        if not customers:
            raise HTTPException(
                status_code=404,
                detail="No premium customers found with account balance greater than $10,000",
            )
        return customers

    # GET /api/customers/{customer_id}
    async def get_customer(self, customer_id: int) -> CustomerOut:
        """Get a customer by ID."""
        customer = self.service.get_customer(customer_id)
        if not customer:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )
        return customer

    # PUT /api/customers/{customer_id}
    async def update_customer(
        self, customer_id: int, customer_in: CustomerIn
    ) -> CustomerOut:
        """Update an existing customer."""
        customer = self.service.update_customer(customer_id, customer_in)
        if not customer:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )
        return customer

    # DELETE /api/customers/{customer_id}
    async def delete_customer(self, customer_id: int) -> None:
        """Delete a customer."""
        success = self.service.delete_customer(customer_id)
        if not success:
            raise HTTPException(
                status_code=404, detail=f"Customer with id {customer_id} not found"
            )

