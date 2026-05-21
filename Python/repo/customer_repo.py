"""Repository for customer data persistence using MongoDB."""
from __future__ import annotations
from typing import Optional

from domain.customer import Customer
from domain.account import Account
from repo.mongo_connection import (
    customers_collection,
    accounts_collection,
    init_indexes,
)


class CustomerRepo:
    """Repository for managing customer data with MongoDB."""

    def __init__(self):
        """Initialize the repository and create indexes."""
        init_indexes()
        self._next_customer_id = self._get_next_id("customers")
        self._next_account_id = self._get_next_id("accounts")

    def _get_next_id(self, collection_name: str) -> int:
        """Get the next available ID for a collection."""
        collection = (
            customers_collection if collection_name == "customers" else accounts_collection
        )
        max_doc = collection.find_one(sort=[("id", -1)])
        return (max_doc["id"] + 1) if max_doc else 1

    def create(self, name: str, account: Account) -> Customer:
        """Create and store a new customer with account."""
        account_data = {
            "id": self._next_account_id,
            "account_type": account.get_account_type(),
            "balance": account.get_balance(),
        }
        accounts_collection.insert_one(account_data)
        account.set_id(account_data["id"])
        self._next_account_id += 1

        customer_data = {
            "id": self._next_customer_id,
            "name": name,
            "account_id": account_data["id"],
        }
        customers_collection.insert_one(customer_data)
        self._next_customer_id += 1

        return Customer(
            id=customer_data["id"],
            name=customer_data["name"],
            account=account,
        )

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """Find a customer by their ID."""
        customer_doc = customers_collection.find_one({"id": customer_id})
        if not customer_doc:
            return None

        account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
        if not account_doc:
            return None

        account = Account(
            id=account_doc["id"],
            account_type=account_doc["account_type"],
            balance=account_doc["balance"],
        )

        return Customer(
            id=customer_doc["id"],
            name=customer_doc["name"],
            account=account,
        )

    def find_all(self) -> list[Customer]:
        """Get all customers."""
        customers = []
        for customer_doc in customers_collection.find().sort("id", 1):
            account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
            account = Account(
                id=account_doc["id"],
                account_type=account_doc["account_type"],
                balance=account_doc["balance"],
            )
            customers.append(
                Customer(
                    id=customer_doc["id"],
                    name=customer_doc["name"],
                    account=account,
                )
            )
        return customers

    def find_balance_minimum(self, balance: float) -> list[Customer]:
        """Get all customers with specified or more account balance."""
        accounts = accounts_collection.find({"balance": {"$gte": balance}})
        account_ids = [acc["id"] for acc in accounts]

        customers = []
        for customer_doc in customers_collection.find(
            {"account_id": {"$in": account_ids}}
        ).sort("id", 1):
            account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
            account = Account(
                id=account_doc["id"],
                account_type=account_doc["account_type"],
                balance=account_doc["balance"],
            )
            customers.append(
                Customer(
                    id=customer_doc["id"],
                    name=customer_doc["name"],
                    account=account,
                )
            )
        return customers

    def get_premium(self) -> list[Customer]:
        """Get all premium customers (account balance > 10000)."""
        return self.find_balance_minimum(10000.01)

    def update(self, customer_id: int, name: str, account: Account) -> Optional[Customer]:
        """Update an existing customer."""
        customer_doc = customers_collection.find_one({"id": customer_id})
        if not customer_doc:
            return None

        customers_collection.update_one(
            {"id": customer_id},
            {"$set": {"name": name}},
        )

        account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
        if account_doc:
            accounts_collection.update_one(
                {"id": account_doc["id"]},
                {
                    "$set": {
                        "account_type": account.get_account_type(),
                        "balance": account.get_balance(),
                    }
                },
            )

        return self.find_by_id(customer_id)

    def delete(self, customer_id: int) -> bool:
        """Delete a customer."""
        customer_doc = customers_collection.find_one({"id": customer_id})
        if not customer_doc:
            return False

        accounts_collection.delete_one({"id": customer_doc["account_id"]})
        customers_collection.delete_one({"id": customer_id})

        return True

    def clear_all(self):
        """Clear all data from collections (useful for testing)."""
        customers_collection.delete_many({})
        accounts_collection.delete_many({})
        self._next_customer_id = 1
        self._next_account_id = 1

