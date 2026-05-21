"""Business logic for auth, profile management, and admin operations."""
from __future__ import annotations

from fastapi import HTTPException, status

from models import (
    AdminAccountOut,
    AdminCustomerOut,
    AuthResponse,
    ProfileOut,
    RegisterIn,
)
from repo.auth_repo import AuthRepo
from utilities.auth import (
    create_session_token,
    hash_password,
    require_register_token,
    verify_password,
)


class AuthService:
    """Service layer for registration, login, and account management."""

    def __init__(self, repo: AuthRepo):
        self.repo = repo

    def register(self, payload: RegisterIn, role: str) -> AuthResponse:
        require_register_token(payload.register_token)

        if role == "customer" and payload.account_type is None:
            payload.account_type = "savings"
        if role == "customer" and payload.balance is None:
            payload.balance = 0.0

        password_hash = hash_password(payload.password)
        try:
            user_doc = self.repo.create_user(
                name=payload.name,
                password_hash=password_hash,
                role=role,
                account_type=payload.account_type,
                balance=payload.balance,
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

        token = create_session_token()
        self.repo.create_session(user_doc["id"], token)
        profile = self.repo.get_profile(user_doc)
        return AuthResponse(token=token, profile=ProfileOut(**profile))

    def login(self, name: str, password: str, role: str) -> AuthResponse:
        user_doc = self.repo.find_user_for_login(name, role)
        if not user_doc or not verify_password(password, user_doc["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid name or password",
            )

        token = create_session_token()
        self.repo.create_session(user_doc["id"], token)
        profile = self.repo.get_profile(user_doc)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account profile not found",
            )
        return AuthResponse(token=token, profile=ProfileOut(**profile))

    def authenticate_token(self, token: str) -> dict:
        user_doc = self.repo.get_user_by_token(token)
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
            )
        return user_doc

    def logout(self, token: str) -> None:
        self.repo.delete_session(token)

    def get_profile(self, user_doc: dict) -> ProfileOut:
        profile = self.repo.get_profile(user_doc)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account profile not found",
            )
        return ProfileOut(**profile)

    def update_name(self, user_doc: dict, new_name: str) -> ProfileOut:
        if not new_name or not new_name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")

        try:
            updated = self.repo.update_name(user_doc, new_name)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

        return self.get_profile(updated)

    def update_password(self, user_doc: dict, password: str) -> None:
        password_hash = hash_password(password)
        self.repo.update_password(user_doc["id"], password_hash)

    def adjust_balance(self, user_doc: dict, amount: float) -> ProfileOut:
        if amount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Adjustment amount cannot be zero",
            )
        try:
            updated = self.repo.adjust_balance(user_doc, amount)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account profile not found",
            )
        return self.get_profile(updated)

    def delete_self(self, user_doc: dict) -> None:
        self.repo.delete_user(user_doc)

    def require_admin(self, user_doc: dict) -> None:
        if user_doc.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

    def list_customers(self, user_doc: dict) -> list[AdminCustomerOut]:
        self.require_admin(user_doc)
        return [self._customer_to_admin_out(c) for c in self.repo.list_customers_for_admin()]

    def list_admins(self, user_doc: dict) -> list[AdminAccountOut]:
        self.require_admin(user_doc)
        return [AdminAccountOut(**row) for row in self.repo.list_admins_for_admin()]

    def admin_delete_customer(self, user_doc: dict, customer_id: int) -> None:
        self.require_admin(user_doc)
        deleted = self.repo.admin_delete_customer(customer_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with id {customer_id} not found",
            )

    @staticmethod
    def _customer_to_admin_out(customer) -> AdminCustomerOut:
        account = customer.get_account()
        return AdminCustomerOut(
            id=customer.get_id(),
            name=customer.get_name(),
            account={
                "id": account.get_id(),
                "account_type": account.get_account_type(),
                "balance": account.get_balance(),
            },
        )
