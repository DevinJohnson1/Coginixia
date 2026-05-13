"""
Customer domain class with constructor, getters, and setters
"""


class Customer:
    """Represents a customer entity."""

    def __init__(self, id: int, name: str, salary: float):
        """
        Constructor for Customer.

        Args:
            id: Unique customer identifier
            name: Customer's name
            salary: Customer's salary
        """
        self._id = id
        self._name = name
        self._salary = salary

    # Getters
    def get_id(self) -> int:
        """Get customer ID."""
        return self._id

    def get_name(self) -> str:
        """Get customer name."""
        return self._name

    def get_salary(self) -> float:
        """Get customer salary."""
        return self._salary

    # Setters
    def set_id(self, id: int) -> None:
        """Set customer ID."""
        self._id = id

    def set_name(self, name: str) -> None:
        """Set customer name."""
        self._name = name

    def set_salary(self, salary: float) -> None:
        """Set customer salary."""
        self._salary = salary

    def to_dict(self) -> dict:
        """Convert customer to dictionary."""
        return {
            "id": self._id,
            "name": self._name,
            "salary": self._salary,
        }

