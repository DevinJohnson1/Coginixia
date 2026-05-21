"""Consolidated backend test suite for auth utilities, auth service, and customer service."""
from __future__ import annotations

from typing import Optional

import pytest
from fastapi import HTTPException, status

from models import RegisterIn
from services.auth_service import AuthService
from utilities.auth import require_path_secret


class FakeAuthRepo:
    """In-memory repo stub for AuthService unit tests."""

    def __init__(self):
        self.next_user_id = 1
        self.users = {}
        self.sessions = {}
        self.customer_rows = []
        self.admin_rows = []
        self.fail_duplicate = False

    def create_user(
        self,
        name: str,
        password_hash: str,
        role: str,
        account_type: Optional[str] = None,
        balance: Optional[float] = None,
    ) -> dict:
        if self.fail_duplicate:
            raise ValueError("An account with that name already exists")

        user_doc = {
            "id": self.next_user_id,
            "name": name,
            "password_hash": password_hash,
            "role": role,
            "customer_id": self.next_user_id if role == "customer" else None,
            "admin_id": self.next_user_id if role == "admin" else None,
        }
        self.next_user_id += 1
        self.users[user_doc["id"]] = user_doc
        return user_doc

    def create_session(self, user_id: int, token: str) -> None:
        self.sessions[token] = user_id

    def find_user_for_login(self, name: str, role: str) -> Optional[dict]:
        for user_doc in self.users.values():
            if user_doc["name"] == name and user_doc["role"] == role:
                return user_doc
        return None

    def get_profile(self, user_doc: dict) -> dict:
        if user_doc["role"] == "customer":
            return {
                "user": {
                    "id": user_doc["id"],
                    "name": user_doc["name"],
                    "role": user_doc["role"],
                },
                "entity_id": user_doc["customer_id"] or user_doc["id"],
                "account": {
                    "id": 1,
                    "account_type": "savings",
                    "balance": 100.0,
                },
            }

        return {
            "user": {
                "id": user_doc["id"],
                "name": user_doc["name"],
                "role": user_doc["role"],
            },
            "entity_id": user_doc["admin_id"] or user_doc["id"],
            "account": None,
        }

    def get_user_by_token(self, token: str) -> Optional[dict]:
        user_id = self.sessions.get(token)
        if not user_id:
            return None
        return self.users.get(user_id)

    def delete_session(self, token: str) -> None:
        self.sessions.pop(token, None)

    def update_name(self, user_doc: dict, new_name: str) -> dict:
        updated = dict(user_doc)
        updated["name"] = new_name
        self.users[user_doc["id"]] = updated
        return updated

    def update_password(self, user_id: int, password_hash: str) -> None:
        self.users[user_id]["password_hash"] = password_hash

    def adjust_balance(self, user_doc: dict, amount: float) -> Optional[dict]:
        if user_doc["role"] != "customer":
            raise ValueError("Admins do not have account balances")
        return user_doc

    def delete_user(self, user_doc: dict) -> None:
        self.users.pop(user_doc["id"], None)

    def list_customers_for_admin(self):
        return self.customer_rows

    def list_admins_for_admin(self):
        return self.admin_rows

    def admin_delete_customer(self, customer_id: int) -> bool:
        return False


@pytest.fixture
def auth_service(monkeypatch):
    monkeypatch.setenv("REGISTER_TOKEN", "register-token")
    return AuthService(FakeAuthRepo())


# Auth utility tests

def test_path_secret_valid(monkeypatch):
    monkeypatch.setenv("API_PATH_SECRET", "super-secret")
    require_path_secret("super-secret")


def test_path_secret_missing_env_raises(monkeypatch):
    monkeypatch.delenv("API_PATH_SECRET", raising=False)

    with pytest.raises(HTTPException) as exc:
        require_path_secret("anything")

    assert exc.value.status_code == 500


def test_path_secret_invalid_raises(monkeypatch):
    monkeypatch.setenv("API_PATH_SECRET", "super-secret")

    with pytest.raises(HTTPException) as exc:
        require_path_secret("wrong-secret")

    assert exc.value.status_code == 401


# Customer service tests

def test_create_customer(customer_service, sample_customer_in):
    result = customer_service.create_customer(sample_customer_in)
    assert result.name == "Test Customer"
    assert result.account.balance == 50000.0
    assert result.account.account_type == "savings"


def test_get_all_customers(populated_service):
    customers = populated_service.get_all_customers()
    assert len(customers) == 3
    assert customers[0].name == "Alice Johnson"


def test_get_premium_customers(populated_service):
    premium = populated_service.get_premium()
    assert len(premium) == 2
    assert premium[0].name == "Alice Johnson"
    assert premium[1].name == "Bob Smith"


def test_get_salary_minimum(populated_service):
    result = populated_service.get_salary_minimum(10000)
    assert len(result) == 3


def test_get_customer_by_id(populated_service):
    customer = populated_service.get_customer(1)
    assert customer is not None
    assert customer.name == "Alice Johnson"


def test_get_nonexistent_customer(customer_service):
    customer = customer_service.get_customer(999)
    assert customer is None


def test_update_customer(customer_service, sample_customer_in):
    created = customer_service.create_customer(sample_customer_in)
    updated_data = sample_customer_in
    updated_data.name = "Updated Name"
    updated = customer_service.update_customer(created.id, updated_data)
    assert updated is not None
    assert updated.name == "Updated Name"


def test_delete_customer(customer_service, sample_customer_in):
    created = customer_service.create_customer(sample_customer_in)
    deleted = customer_service.delete_customer(created.id)
    assert deleted is True
    retrieved = customer_service.get_customer(created.id)
    assert retrieved is None


# Auth service tests

def test_register_customer_applies_default_account_values(auth_service):
    payload = RegisterIn(name="Ada", password="strong-pass", register_token="register-token")

    response = auth_service.register(payload, role="customer")

    assert response.profile.user.name == "Ada"
    assert response.profile.account is not None
    assert response.profile.account.account_type == "savings"
    assert payload.balance == 0.0


def test_register_duplicate_user_returns_conflict(auth_service):
    auth_service.repo.fail_duplicate = True

    with pytest.raises(HTTPException) as exc:
        auth_service.register(
            RegisterIn(name="Ada", password="strong-pass", register_token="register-token"),
            role="customer",
        )

    assert exc.value.status_code == status.HTTP_409_CONFLICT


def test_login_with_wrong_password_returns_unauthorized(auth_service):
    auth_service.register(
        RegisterIn(name="Ada", password="strong-pass", register_token="register-token"),
        role="customer",
    )

    with pytest.raises(HTTPException) as exc:
        auth_service.login("Ada", "incorrect", role="customer")

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_adjust_balance_zero_amount_rejected(auth_service):
    user_doc = {"id": 1, "name": "Ada", "role": "customer", "customer_id": 1}

    with pytest.raises(HTTPException) as exc:
        auth_service.adjust_balance(user_doc, amount=0)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


def test_customer_cannot_access_admin_list(auth_service):
    user_doc = {"id": 1, "name": "Ada", "role": "customer", "customer_id": 1}

    with pytest.raises(HTTPException) as exc:
        auth_service.list_admins(user_doc)

    assert exc.value.status_code == status.HTTP_403_FORBIDDEN


def test_register_rejects_invalid_token(auth_service):
    with pytest.raises(HTTPException) as exc:
        auth_service.register(
            RegisterIn(name="Ada", password="strong-pass", register_token="wrong-token"),
            role="customer",
        )

    assert exc.value.status_code == status.HTTP_403_FORBIDDEN


