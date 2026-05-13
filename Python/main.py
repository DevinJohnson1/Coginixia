# ============================================================
# Customers RESTful API — Structured Architecture
# ============================================================
# Run with:  uvicorn main:app --reload
# Docs at:   http://127.0.0.1:8000/docs
# ============================================================
from fastapi import FastAPI
from repo import CustomerRepo
from services import CustomerService
from controllers import CustomerController, router
from domain.account import Account
# --- Create the FastAPI app instance ---
app = FastAPI(title="Customers RESTful API")
# --- Initialize repository, service, and controller ---
customer_repo = CustomerRepo()
customer_service = CustomerService(customer_repo)
customer_controller = CustomerController(customer_service)
# --- Populate default customers with accounts ---
default_customers = [
    {"name": "Alice Johnson", "account_type": "savings", "balance": 15000},
    {"name": "Bob Smith", "account_type": "checking", "balance": 10500},
    {"name": "Carol Martinez", "account_type": "savings", "balance": 7250},
    {"name": "David Lee", "account_type": "checking", "balance": 3800},
    {"name": "Emma Wilson", "account_type": "savings", "balance": 1000},
]
for i, customer in enumerate(default_customers, start=1):
    account = Account(id=i, account_type=customer["account_type"], balance=customer["balance"])
    customer_repo.create(customer["name"], account)
# --- Include the customer router ---
app.include_router(router)
# ============================================================
# Health check endpoint
# ============================================================
@app.get("/")
def health_check():
    return {"message": "Customers API is running", "status": "healthy"}
