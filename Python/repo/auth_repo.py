"""Repository for authentication, sessions, and admin management."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from domain.account import Account
from domain.customer import Customer
from repo.mongo_connection import (
    accounts_collection,
    admins_collection,
    customers_collection,
    sessions_collection,
    users_collection,
    init_indexes,
)


class AuthRepo:
    """Data access for users, sessions, and role-specific entities."""

    def __init__(self):
        init_indexes()
        self._next_user_id = self._get_next_id(users_collection)
        self._next_admin_id = self._get_next_id(admins_collection)
        self._next_customer_id = self._get_next_id(customers_collection)
        self._next_account_id = self._get_next_id(accounts_collection)

    @staticmethod
    def _get_next_id(collection) -> int:
        max_doc = collection.find_one(sort=[("id", -1)])
        return (max_doc["id"] + 1) if max_doc else 1

    @staticmethod
    def _normalize_username(name: str) -> str:
        return name.strip().lower()

    def _create_account(self, account_type: str, balance: float) -> dict:
        account_doc = {
            "id": self._next_account_id,
            "account_type": account_type,
            "balance": float(balance),
        }
        accounts_collection.insert_one(account_doc)
        self._next_account_id += 1
        return account_doc

    def create_user(
        self,
        name: str,
        password_hash: str,
        role: str,
        account_type: str | None = None,
        balance: float | None = None,
    ) -> dict:
        clean_name = name.strip()
        username = self._normalize_username(clean_name)
        if users_collection.find_one({"username": username}):
            raise ValueError("An account with that name already exists")

        role_ref = {}

        if role == "customer":
            existing_customer = customers_collection.find_one({"name": clean_name})
            if existing_customer:
                role_ref["customer_id"] = existing_customer["id"]
            else:
                if not account_type:
                    raise ValueError("Customers must include an account_type")
                if balance is None:
                    raise ValueError("Customers must include a balance")

                account_doc = self._create_account(account_type, balance)
                customer_doc = {
                    "id": self._next_customer_id,
                    "name": clean_name,
                    "account_id": account_doc["id"],
                }
                customers_collection.insert_one(customer_doc)
                self._next_customer_id += 1
                role_ref["customer_id"] = customer_doc["id"]

        elif role == "admin":
            existing_admin = admins_collection.find_one({"name": clean_name})
            if existing_admin:
                role_ref["admin_id"] = existing_admin["id"]
            else:
                admin_doc = {
                    "id": self._next_admin_id,
                    "name": clean_name,
                }
                admins_collection.insert_one(admin_doc)
                self._next_admin_id += 1
                role_ref["admin_id"] = admin_doc["id"]
        else:
            raise ValueError("Unsupported role")

        user_doc = {
            "id": self._next_user_id,
            "name": clean_name,
            "username": username,
            "password_hash": password_hash,
            "role": role,
            **role_ref,
        }
        users_collection.insert_one(user_doc)
        self._next_user_id += 1
        return user_doc

    def find_user_for_login(self, name: str, role: str) -> Optional[dict]:
        return users_collection.find_one(
            {"username": self._normalize_username(name), "role": role}
        )

    def find_user_by_id(self, user_id: int) -> Optional[dict]:
        return users_collection.find_one({"id": user_id})

    def create_session(self, user_id: int, token: str) -> None:
        sessions_collection.insert_one(
            {
                "token": token,
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc),
            }
        )

    def get_user_by_token(self, token: str) -> Optional[dict]:
        session = sessions_collection.find_one({"token": token})
        if not session:
            return None
        return self.find_user_by_id(session["user_id"])

    def delete_session(self, token: str) -> None:
        sessions_collection.delete_one({"token": token})

    def delete_sessions_for_user(self, user_id: int) -> None:
        sessions_collection.delete_many({"user_id": user_id})

    def get_profile(self, user_doc: dict) -> Optional[dict]:
        entity_id = None
        account_payload = None

        if user_doc["role"] == "customer":
            customer_doc = customers_collection.find_one({"id": user_doc.get("customer_id")})
            if not customer_doc:
                return None
            entity_id = customer_doc["id"]
            account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
            if not account_doc:
                return None
            name = customer_doc["name"]
            account_payload = {
                "id": account_doc["id"],
                "account_type": account_doc["account_type"],
                "balance": account_doc["balance"],
            }
        else:
            admin_doc = admins_collection.find_one({"id": user_doc.get("admin_id")})
            if not admin_doc:
                return None
            entity_id = admin_doc["id"]
            name = admin_doc["name"]

        return {
            "user": {
                "id": user_doc["id"],
                "name": name,
                "role": user_doc["role"],
            },
            "entity_id": entity_id,
            "account": account_payload,
        }

    def update_name(self, user_doc: dict, new_name: str) -> Optional[dict]:
        normalized = self._normalize_username(new_name)
        existing = users_collection.find_one({"username": normalized})
        if existing and existing["id"] != user_doc["id"]:
            raise ValueError("An account with that name already exists")

        users_collection.update_one(
            {"id": user_doc["id"]},
            {"$set": {"name": new_name.strip(), "username": normalized}},
        )

        if user_doc["role"] == "customer":
            customers_collection.update_one(
                {"id": user_doc["customer_id"]},
                {"$set": {"name": new_name.strip()}},
            )
        else:
            admins_collection.update_one(
                {"id": user_doc["admin_id"]},
                {"$set": {"name": new_name.strip()}},
            )

        return self.find_user_by_id(user_doc["id"])

    def update_password(self, user_id: int, password_hash: str) -> None:
        users_collection.update_one({"id": user_id}, {"$set": {"password_hash": password_hash}})

    def adjust_balance(self, user_doc: dict, amount: float) -> Optional[dict]:
        if user_doc["role"] != "customer":
            raise ValueError("Admins do not have account balances")

        owner = customers_collection.find_one({"id": user_doc["customer_id"]})
        if not owner:
            return None

        account_doc = accounts_collection.find_one({"id": owner["account_id"]})
        if not account_doc:
            return None

        new_balance = float(account_doc["balance"]) + float(amount)
        if new_balance < 0:
            raise ValueError("Insufficient funds: balance cannot go below zero")

        accounts_collection.update_one(
            {"id": account_doc["id"]},
            {"$set": {"balance": new_balance}},
        )
        return self.find_user_by_id(user_doc["id"])

    def delete_user(self, user_doc: dict) -> None:
        if user_doc["role"] == "customer":
            customer = customers_collection.find_one({"id": user_doc.get("customer_id")})
            if customer:
                accounts_collection.delete_one({"id": customer["account_id"]})
                customers_collection.delete_one({"id": customer["id"]})
        else:
            admin = admins_collection.find_one({"id": user_doc.get("admin_id")})
            if admin:
                admins_collection.delete_one({"id": admin["id"]})

        self.delete_sessions_for_user(user_doc["id"])
        users_collection.delete_one({"id": user_doc["id"]})

    def list_customers_for_admin(self) -> list[Customer]:
        customers = []
        for customer_doc in customers_collection.find().sort("id", 1):
            account_doc = accounts_collection.find_one({"id": customer_doc["account_id"]})
            if not account_doc:
                continue
            customers.append(
                Customer(
                    id=customer_doc["id"],
                    name=customer_doc["name"],
                    account=Account(
                        id=account_doc["id"],
                        account_type=account_doc["account_type"],
                        balance=account_doc["balance"],
                    ),
                )
            )
        return customers

    def list_admins_for_admin(self) -> list[dict]:
        rows = []
        for admin_doc in admins_collection.find().sort("id", 1):
            user_doc = users_collection.find_one({"admin_id": admin_doc["id"], "role": "admin"})
            if not user_doc:
                continue
            rows.append(
                {
                    "id": admin_doc["id"],
                    "user_id": user_doc["id"],
                    "name": admin_doc["name"],
                }
            )
        return rows

    def admin_delete_customer(self, customer_id: int) -> bool:
        customer_doc = customers_collection.find_one({"id": customer_id})
        if not customer_doc:
            return False

        accounts_collection.delete_one({"id": customer_doc["account_id"]})
        customers_collection.delete_one({"id": customer_id})

        user_doc = users_collection.find_one({"customer_id": customer_id, "role": "customer"})
        if user_doc:
            self.delete_sessions_for_user(user_doc["id"])
            users_collection.delete_one({"id": user_doc["id"]})
        return True
