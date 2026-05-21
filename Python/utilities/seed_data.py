"""
Seed data utility for initializing default customers
"""
import os

DEFAULT_CUSTOMER_SEED_PASSWORD = os.getenv(
    "DEFAULT_CUSTOMER_SEED_PASSWORD", "ChangeMeCustomerSeed123!"
)
DEFAULT_ADMIN_SEED_PASSWORD = os.getenv(
    "DEFAULT_ADMIN_SEED_PASSWORD", "ChangeMeAdminSeed123!"
)

# Default customers with auth and account fields.
# Kept backward-compatible with legacy startup code that reads name/account_type/balance.
SEED_CUSTOMERS = [
    {
        "name": "Alice Johnson",
        "role": "customer",
        "password": DEFAULT_CUSTOMER_SEED_PASSWORD,
        "account_type": "savings",
        "balance": 15000
    },
    {
        "name": "Bob Smith",
        "role": "customer",
        "password": DEFAULT_CUSTOMER_SEED_PASSWORD,
        "account_type": "checking",
        "balance": 12000
    },
    {
        "name": "Carol Martinez",
        "role": "customer",
        "password": DEFAULT_CUSTOMER_SEED_PASSWORD,
        "account_type": "savings",
        "balance": 10000
    }
]


# Default admins for the new auth/admin flows.
SEED_ADMINS = [
    {
        "name": "Admin One",
        "role": "admin",
        "password": DEFAULT_ADMIN_SEED_PASSWORD,
    },
    {
        "name": "Admin Two",
        "role": "admin",
        "password": DEFAULT_ADMIN_SEED_PASSWORD,
    },
]
