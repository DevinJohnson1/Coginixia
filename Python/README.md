# Customers RESTful API — FastAPI with Structured Architecture

A RESTful API built with FastAPI featuring a clean separation of concerns.  
Includes models, repository, service, and controller layers for both Customer and Account entities.

---

## Project Structure

```
Python/
├── main.py                  # FastAPI application entry point
├── customer.py              # Customer domain model (constructor, getters, setters)
├── account.py               # Account domain model (constructor, getters, setters)
├── models.py                # Pydantic validation models (CustomerIn, CustomerOut, AccountIn, AccountOut)
├── customer_repo.py         # Repository layer for customer data persistence
├── account_repo.py          # Repository layer for account data persistence
├── customer_service.py      # Service layer for customer business logic
├── customer_controller.py   # Controller layer with API routes
└── requirements.txt         # Python dependencies
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

The `--reload` flag makes the server restart automatically whenever you save files — great for development.

---

## API Endpoints

| Method | Path                           | Description                     |
|--------|--------------------------------|---------------------------------|
| GET    | `/`                            | Health check                    |
| POST   | `/api/customers`               | Create a new customer           |
| GET    | `/api/customers`               | List all customers              |
| GET    | `/api/customers/{id}`          | Get a specific customer         |
| GET    | `/api/customers/balance/min/n` | Find customers with min balance |
| PUT    | `/api/customers/{id}`          | Update a customer               |
| DELETE | `/api/customers/{id}`          | Delete a customer               |

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

### Create a Customer (POST /api/customers)
```bash
curl -X POST http://localhost:8000/api/customers \
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
curl http://localhost:8000/api/customers
```

### Get a Specific Customer (GET /api/customers/1)
```bash
curl http://localhost:8000/api/customers/1
```

### Find Customers with Minimum Balance (GET /api/customers/balance/min/80000)
```bash
curl http://localhost:8000/api/customers/balance/min/80000
```

### Update a Customer (PUT /api/customers/1)
```bash
curl -X PUT http://localhost:8000/api/customers/1 \
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
curl -X DELETE http://localhost:8000/api/customers/1
```

---

## Example Request & Response

### POST /api/customers

**Request:**
```json
{
  "name": "Alice Johnson",
  "account": {
    "account_type": "savings",
    "balance": 75000
  }
}
```

**Response** (HTTP 201 Created):
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

### GET /api/customers

**Response** (HTTP 200 OK):
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
    "id": 2,
    "name": "Bob Smith",
    "account": {
      "id": 2,
      "account_type": "checking",
      "balance": 65000
    }
  }
]
```

### GET /api/customers/1

**Response** (HTTP 200 OK):
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

### PUT /api/customers/1

**Request:**
```json
{
  "name": "Alice Johnson",
  "account": {
    "account_type": "savings",
    "balance": 80000
  }
}
```

**Response** (HTTP 200 OK):
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "account": {
    "id": 1,
    "account_type": "savings",
    "balance": 80000
  }
}
```

### DELETE /api/customers/1

**Response** (HTTP 204 No Content):
```
(empty body)
```

---

## Architecture Overview

This project follows a **layered architecture** pattern with separation between Customer and Account:

### 1. **Customer Domain Model** (`customer.py`)
- Represents the core customer entity
- Includes constructor, getters, and setters for `id`, `name`, and `account`
- References an Account object

### 2. **Account Domain Model** (`account.py`)
- Represents an account entity
- Includes constructor, getters, and setters for `id`, `account_type`, and `balance`
- Independent from customer logic

### 3. **Pydantic Models** (`models.py`)
- `AccountIn`: Validation schema for account input (account_type, balance)
- `AccountOut`: Response schema for accounts (id, account_type, balance)
- `CustomerIn`: Validation schema for customer input (name, account)
- `CustomerOut`: Response schema for customers (id, name, account)
- Automatic type validation and error handling

### 4. **Repository Layer** (`customer_repo.py`, `account_repo.py`)
- Handles data persistence (in-memory dictionaries)
- Customer repo methods: `create()`, `find_by_id()`, `find_all()`, `find_balance_minimum()`, `update()`, `delete()`
- Account repo methods: `create()`, `find_by_id()`, `find_all()`, `update()`, `delete()`
- Single source of truth for data access

### 5. **Service Layer** (`customer_service.py`)
- Implements business logic for customers
- Translates between domain objects and Pydantic models
- Calls repository methods for data access
- Handles account balance minimum queries

### 6. **Controller Layer** (`customer_controller.py`)
- Defines API routes and HTTP endpoints (documented with HTTP method, endpoint path, full URL, and return type)
- Handles request/response mapping
- Implements error handling with appropriate HTTP status codes

### 7. **Main Application** (`main.py`)
- Initializes FastAPI app
- Wires up repository, service, and controller dependencies
- Registers routes
- Populates 5 default customers with accounts (mix of savings and checking accounts)

