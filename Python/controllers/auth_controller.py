"""Authentication and admin FastAPI routes."""
from __future__ import annotations

from fastapi import APIRouter, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials

from models import (
    AdjustBalanceIn,
    AdminAccountOut,
    AdminCustomerOut,
    AuthResponse,
    LoginIn,
    ProfileOut,
    RegisterIn,
    UpdateNameIn,
    UpdatePasswordIn,
)
from services.auth_service import AuthService
from utilities.auth import bearer_scheme, extract_bearer_token


class AuthController:
    """Controller that mounts auth/profile/admin routes."""

    def __init__(self, service: AuthService):
        self.service = service
        self.router = APIRouter(prefix="/api", tags=["auth"])
        self._setup_routes()

    def _setup_routes(self):
        self.router.post("/auth/register/customer", response_model=AuthResponse, status_code=201)(
            self.register_customer
        )
        self.router.post("/auth/register/admin", response_model=AuthResponse, status_code=201)(
            self.register_admin
        )
        self.router.post("/auth/login/customer", response_model=AuthResponse)(self.login_customer)
        self.router.post("/auth/login/admin", response_model=AuthResponse)(self.login_admin)
        self.router.post("/auth/logout", status_code=204)(self.logout)

        self.router.get("/auth/me", response_model=ProfileOut)(self.get_me)
        self.router.patch("/auth/me/name", response_model=ProfileOut)(self.update_name)
        self.router.patch("/auth/me/password", status_code=204)(self.update_password)
        self.router.post("/auth/me/balance/adjust", response_model=ProfileOut)(self.adjust_balance)
        self.router.delete("/auth/me", status_code=204)(self.delete_me)

        self.router.get("/admin/customers", response_model=list[AdminCustomerOut])(self.list_customers)
        self.router.get("/admin/admins", response_model=list[AdminAccountOut])(self.list_admins)
        self.router.delete("/admin/customers/{customer_id}", status_code=204)(
            self.delete_customer
        )

    async def register_customer(self, payload: RegisterIn) -> AuthResponse:
        return self.service.register(payload, role="customer")

    async def register_admin(self, payload: RegisterIn) -> AuthResponse:
        return self.service.register(payload, role="admin")

    async def login_customer(self, payload: LoginIn) -> AuthResponse:
        return self.service.login(payload.name, payload.password, role="customer")

    async def login_admin(self, payload: LoginIn) -> AuthResponse:
        return self.service.login(payload.name, payload.password, role="admin")

    async def logout(
        self,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> Response:
        token = extract_bearer_token(credentials)
        self.service.logout(token)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def get_me(
        self,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> ProfileOut:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        return self.service.get_profile(user_doc)

    async def update_name(
        self,
        payload: UpdateNameIn,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> ProfileOut:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        return self.service.update_name(user_doc, payload.name)

    async def update_password(
        self,
        payload: UpdatePasswordIn,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> Response:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        self.service.update_password(user_doc, payload.password)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def adjust_balance(
        self,
        payload: AdjustBalanceIn,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> ProfileOut:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        return self.service.adjust_balance(user_doc, payload.amount)

    async def delete_me(
        self,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> Response:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        self.service.delete_self(user_doc)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def list_customers(
        self,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> list[AdminCustomerOut]:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        return self.service.list_customers(user_doc)

    async def list_admins(
        self,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> list[AdminAccountOut]:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        return self.service.list_admins(user_doc)

    async def delete_customer(
        self,
        customer_id: int,
        credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
    ) -> Response:
        token = extract_bearer_token(credentials)
        user_doc = self.service.authenticate_token(token)
        self.service.admin_delete_customer(user_doc, customer_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
