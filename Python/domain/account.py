"""
Account domain class with constructor, getters, and setters
"""


class Account:
    """Represents an account entity."""

    def __init__(self, id: int, account_type: str, balance: float):
        """
        Constructor for Account.

        Args:
            id: Unique account identifier
            account_type: Type of account (savings or checking)
            balance: Account balance
        """
        self._id = id
        self._account_type = account_type
        self._balance = balance

    # Getters
    def get_id(self) -> int:
        """Get account ID."""
        return self._id

    def get_account_type(self) -> str:
        """Get account type."""
        return self._account_type

    def get_balance(self) -> float:
        """Get account balance."""
        return self._balance

    # Setters
    def set_id(self, id: int) -> None:
        """Set account ID."""
        self._id = id

    def set_account_type(self, account_type: str) -> None:
        """Set account type."""
        self._account_type = account_type

    def set_balance(self, balance: float) -> None:
        """Set account balance."""
        self._balance = balance

    def to_dict(self) -> dict:
        """Convert account to dictionary."""
        return {
            "id": self._id,
            "account_type": self._account_type,
            "balance": self._balance,
        }

