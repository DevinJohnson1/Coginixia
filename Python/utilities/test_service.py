"""
Service layer tests using fixtures from conftest
"""
import pytest
def test_create_customer(customer_service, sample_customer_in):
    """Test creating a new customer."""
    result = customer_service.create_customer(sample_customer_in)
    assert result.name == "Test Customer"
    assert result.account.balance == 50000.0
    assert result.account.account_type == "savings"
def test_get_all_customers(populated_service):
    """Test retrieving all customers from populated service."""
    customers = populated_service.get_all_customers()
    assert len(customers) == 5
    assert customers[0].name == "Alice Johnson"
def test_get_premium_customers(populated_service):
    """Test getting premium customers (balance > 10000)."""
    premium = populated_service.get_premium()
    # Alice: 15000, Bob: 12000 (both > 10000)
    assert len(premium) == 2
    assert premium[0].name == "Alice Johnson"
    assert premium[1].name == "Bob Smith"
def test_get_salary_minimum(populated_service):
    """Test filtering customers by minimum balance."""
    result = populated_service.get_salary_minimum(10000)
    # Alice: 15000, Bob: 12000, Carol: 10000 (all >= 10000)
    assert len(result) == 3
def test_get_customer_by_id(populated_service):
    """Test retrieving a customer by ID."""
    customer = populated_service.get_customer(1)
    assert customer is not None
    assert customer.name == "Alice Johnson"
def test_get_nonexistent_customer(customer_service):
    """Test retrieving a customer that doesn't exist."""
    customer = customer_service.get_customer(999)
    assert customer is None
def test_update_customer(customer_service, sample_customer_in):
    """Test updating an existing customer."""
    # Create a customer first
    created = customer_service.create_customer(sample_customer_in)
    # Update it
    updated_data = sample_customer_in
    updated_data.name = "Updated Name"
    updated = customer_service.update_customer(created.id, updated_data)
    assert updated is not None
    assert updated.name == "Updated Name"
def test_delete_customer(customer_service, sample_customer_in):
    """Test deleting a customer."""
    created = customer_service.create_customer(sample_customer_in)
    # Delete it
    deleted = customer_service.delete_customer(created.id)
    assert deleted is True
    # Verify it's gone
    retrieved = customer_service.get_customer(created.id)
    assert retrieved is None
