"""
Pytest configuration for utilities package
Defines all fixtures needed for service layer testing
"""
import pytest
from repo import CustomerRepo
from services import CustomerService
from domain.account import Account
from domain.customer import Customer
from models import AccountIn, CustomerIn
from utilities.seed_data import SEED_CUSTOMERS


@pytest.fixture
def customer_repo():
    """Create a fresh CustomerRepo instance for each test."""
    return CustomerRepo()


@pytest.fixture
def customer_service(customer_repo):
    """Create a fresh CustomerService instance for each test."""
    return CustomerService(customer_repo)


@pytest.fixture
def sample_account():
    """Create a sample account for testing."""
    return Account(id=1, account_type="savings", balance=50000.0)


@pytest.fixture
def sample_account_in():
    """Create a sample AccountIn model for testing."""
    return AccountIn(account_type="checking", balance=30000.0)


@pytest.fixture
def sample_customer_in():
    """Create a sample CustomerIn model for testing."""
    return CustomerIn(
        name="Test Customer",
        account=AccountIn(account_type="savings", balance=50000.0)
    )


@pytest.fixture
def populated_repo(customer_repo):
    """Create a repo with pre-populated test customers from SEED_CUSTOMERS."""
    for i, customer_data in enumerate(SEED_CUSTOMERS, start=1):
        account = Account(
            id=i,
            account_type=customer_data["account_type"],
            balance=customer_data["balance"]
        )
        customer_repo.create(customer_data["name"], account)

    return customer_repo


@pytest.fixture
def populated_service(populated_repo):
    """Create a service with pre-populated test customers."""
    return CustomerService(populated_repo)

