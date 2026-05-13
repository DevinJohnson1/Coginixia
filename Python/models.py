"""
Customer models for Pydantic validation
"""
from pydantic import BaseModel


class CustomerIn(BaseModel):
    """Fields the client sends when creating or updating a customer."""
    name: str
    salary: float


class CustomerOut(BaseModel):
    """Fields returned to the client (includes the auto-generated id)."""
    id: int
    name: str
    salary: float

