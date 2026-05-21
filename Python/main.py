# Run with:  uvicorn main:app --reload
# Docs at:   http://127.0.0.1:8000/docs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from repo import CustomerRepo, AuthRepo
from services import CustomerService, AuthService
from utilities import SEED_CUSTOMERS, SEED_ADMINS
from controllers import CustomerController, router
from controllers.auth_controller import AuthController
from utilities.auth import hash_password
from repo.mongo_connection import clear_all_collections
from mangum import Mangum

# Create the FastAPI app instance
app = FastAPI(title="Customers RESTful API")

# Allow local frontend dev servers (Vite/React) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clear database on startup for fresh data
clear_all_collections()

# Initialize repository, service, and controller
customer_repo = CustomerRepo()
customer_service = CustomerService(customer_repo)
customer_controller = CustomerController(customer_service)

auth_repo = AuthRepo()
auth_service = AuthService(auth_repo)
auth_controller = AuthController(auth_service)

def _seed_auth_users() -> None:
    """Seed customer/admin auth users with PBKDF2-hashed passwords."""

    for customer in SEED_CUSTOMERS:
        existing_user = auth_repo.find_user_for_login(customer["name"], "customer")
        if existing_user:
            # Repair legacy plaintext/invalid hashes if present.
            if not str(existing_user.get("password_hash", "")).startswith("pbkdf2_"):
                auth_repo.update_password(existing_user["id"], hash_password(customer["password"]))
            continue

        auth_repo.create_user(
            name=customer["name"],
            password_hash=hash_password(customer["password"]),
            role="customer",
            account_type=customer["account_type"],
            balance=customer["balance"],
        )

    for admin in SEED_ADMINS:
        existing_user = auth_repo.find_user_for_login(admin["name"], "admin")
        if existing_user:
            # Repair legacy plaintext/invalid hashes if present.
            if not str(existing_user.get("password_hash", "")).startswith("pbkdf2_"):
                auth_repo.update_password(existing_user["id"], hash_password(admin["password"]))
            continue

        auth_repo.create_user(
            name=admin["name"],
            password_hash=hash_password(admin["password"]),
            role="admin",
        )


# Seed auth users and repair legacy password hashes on startup.
_seed_auth_users()

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "Customers API is running", "status": "healthy"}

# Include the customer router
app.include_router(router)
app.include_router(auth_controller.router)

# Adding in lambda support
lambda_handler = Mangum(app, lifespan="off")
