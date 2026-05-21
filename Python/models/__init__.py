"""
Pydantic validation models for requests and responses
"""
from pydantic import BaseModel
from typing import Literal


class AccountIn(BaseModel):
    """Fields the client sends when creating or updating an account."""
    account_type: str
    balance: float


class AccountOut(BaseModel):
    """Fields returned to the client for an account (includes the auto-generated id)."""
    id: int
    account_type: str
    balance: float


class CustomerIn(BaseModel):
    """Fields the client sends when creating or updating a customer."""
    name: str
    account: AccountIn


class CustomerOut(BaseModel):
    """Fields returned to the client (includes the auto-generated id)."""
    id: int
    name: str
    account: AccountOut


class RegisterIn(BaseModel):
    """Fields required to register a customer or admin login account."""

    name: str
    password: str
    register_token: str
    account_type: str | None = None
    balance: float | None = None


class LoginIn(BaseModel):
    """Fields required to login to an existing account."""

    name: str
    password: str


class UserOut(BaseModel):
    """Minimal user details returned to clients."""

    id: int
    name: str
    role: Literal["customer", "admin"]


class ProfileOut(BaseModel):
    """Authenticated profile plus account details."""

    user: UserOut
    account: AccountOut | None = None
    entity_id: int


class AuthResponse(BaseModel):
    """Response payload returned from login and registration."""

    token: str
    profile: ProfileOut


class UpdateNameIn(BaseModel):
    """Update a user's login/display name."""

    name: str


class UpdatePasswordIn(BaseModel):
    """Update a user's password."""

    password: str


class AdjustBalanceIn(BaseModel):
    """Adjust account balance by a signed amount."""

    amount: float


class AdminCustomerOut(BaseModel):
    """Customer row for admin management table."""

    id: int
    name: str
    account: AccountOut


class AdminAccountOut(BaseModel):
    """Admin row for admin visibility table."""

    id: int
    user_id: int
    name: str

