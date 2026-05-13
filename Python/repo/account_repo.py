"""
Account repository for data persistence
"""
from domain.account import Account


class AccountRepo:
    """Repository for managing account data."""

    def __init__(self):
        """Initialize the repository with an empty account store."""
        self._accounts: dict[int, Account] = {}
        self._next_id = 1

    def create(self, account_type: str, balance: float) -> Account:
        """
        Create and store a new account.

        Args:
            account_type: Type of account (savings or checking)
            balance: Account balance

        Returns:
            The created Account object
        """
        account = Account(self._next_id, account_type, balance)
        self._accounts[self._next_id] = account
        self._next_id += 1
        return account

    def find_by_id(self, account_id: int) -> Account | None:
        """
        Find an account by its ID.

        Args:
            account_id: The account's ID

        Returns:
            The Account if found, None otherwise
        """
        return self._accounts.get(account_id)

    def find_all(self) -> list[Account]:
        """
        Get all accounts.

        Returns:
            A list of all Account objects
        """
        return list(self._accounts.values())

    def update(self, account_id: int, account_type: str = None, balance: float = None) -> Account | None:
        """
        Update an existing account.

        Args:
            account_id: The account's ID
            account_type: New account type (optional)
            balance: New balance (optional)

        Returns:
            The updated Account if found, None otherwise
        """
        account = self._accounts.get(account_id)
        if account:
            if account_type is not None:
                account.set_account_type(account_type)
            if balance is not None:
                account.set_balance(balance)
        return account

    def delete(self, account_id: int) -> bool:
        """
        Delete an account.

        Args:
            account_id: The account's ID

        Returns:
            True if deleted, False if not found
        """
        if account_id in self._accounts:
            del self._accounts[account_id]
            return True
        return False

