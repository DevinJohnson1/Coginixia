"""
Pydantic validation models for requests and responses
"""
from pydantic import BaseModel


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

