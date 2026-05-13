# ============================================================
# Customers RESTful API — Structured Architecture
# ============================================================
# Run with:  uvicorn main:app --reload
# Docs at:   http://127.0.0.1:8000/docs
# ============================================================

from fastapi import FastAPI
from customer_repo import CustomerRepo
from customer_service import CustomerService
from customer_controller import CustomerController, router

# --- Create the FastAPI app instance ---
app = FastAPI(title="Customers RESTful API")

# --- Initialize repository, service, and controller ---
customer_repo = CustomerRepo()
customer_service = CustomerService(customer_repo)
customer_controller = CustomerController(customer_service)

# --- Populate default customers ---
default_customers = [
    {"name": "Alice Johnson", "salary": 75000},
    {"name": "Bob Smith", "salary": 65000},
    {"name": "Carol Martinez", "salary": 85000},
    {"name": "David Lee", "salary": 70000},
    {"name": "Emma Wilson", "salary": 80000},
]
for customer in default_customers:
    customer_repo.create(customer["name"], customer["salary"])

# --- Include the customer router ---
app.include_router(router)


# ============================================================
# Health check endpoint
# ============================================================
@app.get("/")
def health_check():
    return {"message": "Customers API is running", "status": "healthy"}
