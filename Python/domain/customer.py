"""
Customer domain class with constructor, getters, and setters
"""
from domain.account import Account


class Customer:
    """Represents a customer entity."""

    def __init__(self, id: int, name: str, account: Account):
        """
        Constructor for Customer.

        Args:
            id: Unique customer identifier
            name: Customer's name
            account: Customer's account information
        """
        self._id = id
        self._name = name
        self._account = account

    # Getters
    def get_id(self) -> int:
        """Get customer ID."""
        return self._id

    def get_name(self) -> str:
        """Get customer name."""
        return self._name

    def get_account(self) -> Account:
        """Get customer account."""
        return self._account

    # Setters
    def set_id(self, id: int) -> None:
        """Set customer ID."""
        self._id = id

    def set_name(self, name: str) -> None:
        """Set customer name."""
        self._name = name

    def set_account(self, account: Account) -> None:
        """Set customer account."""
        self._account = account

    def to_dict(self) -> dict:
        """Convert customer to dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "account": self._account.to_dict(),
        }

