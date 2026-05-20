
# Customers RESTful API — FastAPI with Structured Architecture

A RESTful API built with FastAPI featuring a clean separation of concerns.  
Includes models, repository, service, and controller layers for both Customer and Account entities.

---

## Project Structure

```
Python/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
│
├── domain/                          # Domain Models Layer
│   ├── __init__.py
│   ├── customer.py                  # Customer entity (constructor, getters, setters)
│   └── account.py                   # Account entity (constructor, getters, setters)
│
├── models/                          # Pydantic Validation Layer
│   └── __init__.py                  # CustomerIn/Out, AccountIn/Out
│
├── repo/                            # Repository/Data Persistence Layer
│   ├── __init__.py                  # CustomerRepo (CRUD operations)
│   └── account_repo.py              # AccountRepo (CRUD operations)
│
├── services/                        # Service/Business Logic Layer
│   └── __init__.py                  # CustomerService (orchestration & logic)
│
└── controllers/                     # Controller/API Routes Layer
    └── __init__.py                  # CustomerController with all routes
```

---

## Step-by-Step Setup

### 1. Open a terminal and navigate to this folder

```bash
cd path/to/Cognixia/Python
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Mac / Linux**
```bash
source venv/bin/activate
```

**Windows (Command Prompt)**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
venv\Scripts\Activate.ps1
```

> You'll see `(venv)` at the start of your prompt when it's active.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set auth environment variables

```bash
export API_PATH_SECRET="replace-with-a-long-random-string"
```

---

## Running the App

```bash
uvicorn main:app --reload
```

| What               | URL                          |
|--------------------|------------------------------|
| App root           | http://localhost:8000        |
| Interactive Swagger UI | http://localhost:8000/docs |
| Alternative ReDoc  | http://localhost:8000/redoc  |

---

## API Endpoints

| Method | Path                           | Description                          |
|--------|--------------------------------|--------------------------------------|
| GET    | `/`                            | Health check                         |
| POST   | `/api/{secret}/customers`               | Create a new customer                |
| GET    | `/api/{secret}/customers`               | List all customers                   |
| GET    | `/api/{secret}/customers/premium`       | Get premium customers (balance > $10,000)|
| GET    | `/api/{secret}/customers/balance/min/n` | Find customers with minimum balance  |
| GET    | `/api/{secret}/customers/{id}`          | Get a specific customer              |
| PUT    | `/api/{secret}/customers/{id}`          | Update a customer                    |
| DELETE | `/api/{secret}/customers/{id}`          | Delete a customer                    |

---

## Data Models

### Customer
Each customer has the following attributes:

- **id** (integer): Unique identifier, auto-generated
- **name** (string): Customer's full name
- **account** (object): Customer's account information

### Account
Each account has the following attributes:

- **id** (integer): Unique identifier, auto-generated
- **account_type** (string): Type of account (`"savings"` or `"checking"`)
- **balance** (float): Account balance

---

## Sample curl Commands

### Health Check
```bash
curl http://localhost:8000/
```

### Example: List Customers with Path Secret
```bash
SECRET="replace-with-your-api-path-secret"
curl "http://localhost:8000/api/${SECRET}/customers"
```

### Create a Customer (POST /api/customers)
```bash
SECRET="replace-with-your-api-path-secret"
curl -X POST "http://localhost:8000/api/${SECRET}/customers" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "account": {
         "account_type": "savings",
         "balance": 95000
       }
     }'
```

### List All Customers (GET /api/customers)
```bash
SECRET="replace-with-your-api-path-secret"
curl "http://localhost:8000/api/${SECRET}/customers"
```

### Get a Specific Customer (GET /api/customers/1)
```bash
SECRET="replace-with-your-api-path-secret"
curl "http://localhost:8000/api/${SECRET}/customers/1"
```

### Get Premium Customers (GET /api/customers/premium)
```bash
SECRET="replace-with-your-api-path-secret"
curl "http://localhost:8000/api/${SECRET}/customers/premium"
```

### Find Customers with Minimum Balance (GET /api/customers/balance/min/80000)
```bash
SECRET="replace-with-your-api-path-secret"
curl "http://localhost:8000/api/${SECRET}/customers/balance/min/80000"
```

### Update a Customer (PUT /api/customers/1)
```bash
SECRET="replace-with-your-api-path-secret"
curl -X PUT "http://localhost:8000/api/${SECRET}/customers/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "account": {
         "account_type": "checking",
         "balance": 100000
       }
     }'
```

### Delete a Customer (DELETE /api/customers/1)
```bash
SECRET="replace-with-your-api-path-secret"
curl -X DELETE "http://localhost:8000/api/${SECRET}/customers/1"
```
---

## Architecture Overview

This project follows a **clean layered architecture** pattern with separation between Customer and Account:

### 1. **Domain Layer** (`domain/`)
- **Customer** (`domain/customer.py`): Core customer entity with constructor, getters, setters for `id`, `name`, and `account`
- **Account** (`domain/account.py`): Account entity with `id`, `account_type`, and `balance`

### 2. **Pydantic Models** (`models/`)
- `AccountIn/Out`: Validation and response schemas for accounts
- `CustomerIn/Out`: Validation and response schemas for customers
- Automatic type validation and error handling

### 3. **Repository Layer** (`repo/`)
- **CustomerRepo** (`repo/__init__.py`): CRUD operations + `get_premium()` for premium customers
- **AccountRepo** (`repo/account_repo.py`): Account persistence
- Single source of truth for data access

### 4. **Service Layer** (`services/`)
- **CustomerService** (`services/__init__.py`): Business logic
- Translates between domain objects and Pydantic models
- Premium customer queries: `get_premium()` (balance > $10,000)
- Minimum balance queries

### 5. **Controller Layer** (`controllers/`)
- **CustomerController** (`controllers/__init__.py`): API routes with proper documentation
- 8 RESTful endpoints including premium customers
- Error handling with appropriate HTTP status codes

### 6. **Main Application** (`main.py`)
- Initializes FastAPI app
- Wires up repository, service, and controller dependencies
- Registers routes
- Populates 5 default customers with accounts (mix of savings and checking accounts)
