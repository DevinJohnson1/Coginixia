# Run with:  uvicorn main:app --reload
# Docs at:   http://127.0.0.1:8000/docs
from fastapi import FastAPI
from repo import CustomerRepo
from services import CustomerService
from utilities import SEED_CUSTOMERS
from controllers import CustomerController, router
from domain.account import Account

# Create the FastAPI app instance
app = FastAPI(title="Customers RESTful API")

# Initialize repository, service, and controller
customer_repo = CustomerRepo()
customer_service = CustomerService(customer_repo)
customer_controller = CustomerController(customer_service)

# Seed default customers from utilities (only if database is empty)
existing_customers = customer_repo.find_all()
if not existing_customers:
    for i, customer in enumerate(SEED_CUSTOMERS, start=1):
        account = Account(id=i, account_type=customer["account_type"], balance=customer["balance"])
        customer_repo.create(customer["name"], account)

# Include the customer router
app.include_router(router)

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "Customers API is running", "status": "healthy"}
