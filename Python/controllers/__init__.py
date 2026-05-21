"""Controllers (FastAPI routers) for the API."""
from controllers.customer_controller import CustomerController, router
from controllers.auth_controller import AuthController

__all__ = ["CustomerController", "AuthController", "router"]
