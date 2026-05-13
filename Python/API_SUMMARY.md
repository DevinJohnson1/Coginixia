# Complete API Summary
## All Available Endpoints
### 1. **Health Check**
```
GET /
Returns: {"message": "Customers API is running", "status": "healthy"}
```
### 2. **Create Customer**
```
POST /api/customers
Input: {"name": "string", "account": {"account_type": "savings|checking", "balance": float}}
Returns: CustomerOut with generated ID
Status: 201 Created
```
### 3. **Get All Customers**
```
GET /api/customers
Returns: list[CustomerOut]
Status: 200 OK
```
### 4. **Get Premium Customers** ⭐ NEW
```
GET /api/customers/premium
Returns: list[CustomerOut] - customers with balance > $10,000
Status: 200 OK or 404 Not Found
```
### 5. **Get Customers by Minimum Balance**
```
GET /api/customers/balance/min/{balance}
Returns: list[CustomerOut] - customers with balance ≥ specified amount
Status: 200 OK or 404 Not Found
```
### 6. **Get Single Customer**
```
GET /api/customers/{id}
Returns: CustomerOut
Status: 200 OK or 404 Not Found
```
### 7. **Update Customer**
```
PUT /api/customers/{id}
Input: {"name": "string", "account": {"account_type": "string", "balance": float}}
Returns: updated CustomerOut
Status: 200 OK or 404 Not Found
```
### 8. **Delete Customer**
```
DELETE /api/customers/{id}
Returns: (empty)
Status: 204 No Content or 404 Not Found
```
---
## Quick Test Commands
### Health Check
```bash
curl http://localhost:8000/
```
### Get All Customers
```bash
curl http://localhost:8000/api/customers
```
### Get Premium Customers
```bash
curl http://localhost:8000/api/customers/premium
```
### Get Customers with Min Balance
```bash
curl http://localhost:8000/api/customers/balance/min/75000
```
### Create Customer
```bash
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","account":{"account_type":"savings","balance":50000}}'
```
### Update Customer
```bash
curl -X PUT http://localhost:8000/api/customers/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","account":{"account_type":"checking","balance":75000}}'
```
### Delete Customer
```bash
curl -X DELETE http://localhost:8000/api/customers/1
```
---
## Data Model
### Customer
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "account": {
    "id": 1,
    "account_type": "savings",
    "balance": 75000
  }
}
```
### Account Types
- `"savings"` - Savings account
- `"checking"` - Checking account
---
## Premium Tier
**Premium Criteria:** Account balance > $10,000
### Default Premium Customers
- Alice Johnson ($75,000)
- Bob Smith ($65,000)
- Carol Martinez ($85,000)
- David Lee ($70,000)
- Emma Wilson ($80,000)
**Result:** 5 out of 5 are premium! 🎉
---
## HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 204 | No Content - Deleted successfully |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Invalid input |
---
## Interactive Documentation
**Swagger UI:** `http://localhost:8000/docs`
**ReDoc:** `http://localhost:8000/redoc`
---
## Architecture
```
FastAPI Application
├── Controllers (HTTP Routes)
├── Services (Business Logic)
├── Repositories (Data Access)
└── Domain Models (Entities)
```
---
## Implementation Summary
✅ **RESTful API** with proper HTTP methods  
✅ **Clean Architecture** with separated layers  
✅ **Error Handling** with meaningful messages  
✅ **Data Validation** with Pydantic models  
✅ **Premium Tier** for customers with balance > $10,000  
✅ **Fully Documented** with inline comments  
✅ **Ready to Deploy** to production  
---
Generated: May 13, 2026
