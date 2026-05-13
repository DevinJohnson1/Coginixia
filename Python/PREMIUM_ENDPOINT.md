# Premium Customers Endpoint
## New Feature: Premium Customers API
A new endpoint has been added to retrieve **premium customers** - those with account balance greater than $10,000.
---
## Endpoint Details
### GET /api/customers/premium
**Description:** Get all customers with account balance > $10,000  
**HTTP Method:** GET  
**Full URL:** `http://localhost:8000/api/customers/premium` OR `BaseURL/api/customers/premium`  
**Returns:** `list[CustomerOut]` - Array of premium customer objects  
---
## Implementation
### Architecture Changes
#### 1. **Repository Layer** (`repo/__init__.py`)
Added `get_premium()` method:
```python
def get_premium(self) -> list[Customer]:
    """Get all premium customers (account balance > 10000)."""
    return [customer for customer in self._customers.values() 
            if customer.get_account().get_balance() > 10000]
```
#### 2. **Service Layer** (`services/__init__.py`)
Added `get_premium()` method:
```python
def get_premium(self) -> list[CustomerOut]:
    """Retrieve all premium customers (account balance > 10000)."""
    customers = self.repo.get_premium()
    return [self._customer_to_out(c) for c in customers]
```
#### 3. **Controller Layer** (`controllers/__init__.py`)
- Added route registration in `_setup_routes()`
- Added `get_premium()` endpoint with error handling:
```python
@router.get("/premium", response_model=list[CustomerOut])
async def get_premium(self) -> list[CustomerOut]:
    """Get all premium customers with balance > 10000."""
    customers = self.service.get_premium()
    if not customers:
        raise HTTPException(
            status_code=404,
            detail="No premium customers found with account balance greater than $10,000"
        )
    return customers
```
---
## API Usage Examples
### Using cURL
```bash
# Get all premium customers
curl http://localhost:8000/api/customers/premium
# Pretty print with jq
curl http://localhost:8000/api/customers/premium | jq '.'
```
### Using Python Requests
```python
import requests
response = requests.get('http://localhost:8000/api/customers/premium')
premium_customers = response.json()
for customer in premium_customers:
    print(f"{customer['name']}: ${customer['account']['balance']}")
```
### Using Postman
1. **Method:** GET
2. **URL:** `http://localhost:8000/api/customers/premium`
3. **Headers:** (none required)
4. **Body:** (empty)
5. **Click Send**
---
## Response Examples
### Success Response (HTTP 200)
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "account": {
      "id": 1,
      "account_type": "savings",
      "balance": 75000
    }
  },
  {
    "id": 3,
    "name": "Carol Martinez",
    "account": {
      "id": 3,
      "account_type": "savings",
      "balance": 85000
    }
  },
  {
    "id": 5,
    "name": "Emma Wilson",
    "account": {
      "id": 5,
      "account_type": "savings",
      "balance": 80000
    }
  }
]
```
### Error Response (HTTP 404)
```json
{
  "detail": "No premium customers found with account balance greater than $10,000"
}
```
---
## Default Data Status
### All 5 Default Customers:
| Customer | Account Type | Balance | Premium? |
|----------|--------------|---------|----------|
| Alice Johnson | savings | $75,000 | ✅ Yes |
| Bob Smith | checking | $65,000 | ✅ Yes |
| Carol Martinez | savings | $85,000 | ✅ Yes |
| David Lee | checking | $70,000 | ✅ Yes |
| Emma Wilson | savings | $80,000 | ✅ Yes |
**Result:** All 5 default customers are premium members!
---
## Premium Criteria
- **Premium Status:** Account balance > $10,000
- **Non-Premium Status:** Account balance ≤ $10,000
---
## All API Endpoints
| HTTP | Path | Description |
|------|------|-------------|
| GET | `/` | Health check |
| POST | `/api/customers` | Create customer |
| GET | `/api/customers` | List all customers |
| **GET** | **`/api/customers/premium`** | **Get premium customers** |
| GET | `/api/customers/balance/min/n` | Find by min balance |
| GET | `/api/customers/{id}` | Get one customer |
| PUT | `/api/customers/{id}` | Update customer |
| DELETE | `/api/customers/{id}` | Delete customer |
---
## Testing the Endpoint
### Quick Test via FastAPI Docs
1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
2. Visit interactive docs:
   ```
   http://localhost:8000/docs
   ```
3. Find **GET /api/customers/premium** endpoint
4. Click "Try it out"
5. Click "Execute"
6. View the premium customers response
---
## Key Features
✅ **Simple & Fast** - No parameters needed  
✅ **Error Handling** - Returns 404 if no premium customers found  
✅ **RESTful** - Follows REST conventions  
✅ **Documented** - Fully documented with HTTP method, endpoint, and return type  
✅ **Tested** - Verified to work correctly  
✅ **Integrated** - Works with entire layered architecture  
---
## Technical Summary
**Keywords Used:** `get_premium`, `premium`  
**Balance Threshold:** $10,000 (exclusive, > not >=)  
**Response Type:** Array of CustomerOut objects  
**HTTP Status:** 200 OK or 404 Not Found
This endpoint provides a quick way to query premium customers without needing to fetch all customers and filter client-side!
