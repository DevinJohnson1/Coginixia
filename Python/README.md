# Customers RESTful API — FastAPI with Structured Architecture

A RESTful API built with FastAPI featuring a clean separation of concerns.  
Includes models, repository, service, and controller layers.

---

## Project Structure

```
Python/
├── main.py                  # FastAPI application entry point
├── customer.py              # Customer domain model (constructor, getters, setters)
├── models.py                # Pydantic validation models (CustomerIn, CustomerOut)
├── customer_repo.py         # Repository layer for data persistence
├── customer_service.py      # Service layer for business logic
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

| Method | Path                    | Description              |
|--------|-------------------------|--------------------------|
| GET    | `/`                     | Health check             |
| POST   | `/customers`            | Create a new customer    |
| GET    | `/customers`            | List all customers       |
| GET    | `/customers/{id}`       | Get a specific customer  |
| PUT    | `/customers/{id}`       | Update a customer        |
| DELETE | `/customers/{id}`       | Delete a customer        |

Each endpoint is fully documented in `customer_controller.py` with HTTP method, endpoint path, full URL format, and return type information.

---

## Sample curl Commands

### Health Check
```bash
curl http://localhost:8000/
```

### Create a Customer (POST /customers)
```bash
curl -X POST http://localhost:8000/customers \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice Johnson", "salary": 75000}'
```

### List All Customers (GET /customers)
```bash
curl http://localhost:8000/customers
```

### Get a Specific Customer (GET /customers/1)
```bash
curl http://localhost:8000/customers/1
```

### Update a Customer (PUT /customers/1)
```bash
curl -X PUT http://localhost:8000/customers/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice Johnson", "salary": 80000}'
```

### Delete a Customer (DELETE /customers/1)
```bash
curl -X DELETE http://localhost:8000/customers/1
```

---

## Example Request & Response

### POST /customers

**Request:**
```json
{
  "name": "Alice Johnson",
  "salary": 75000
}
```

**Response (HTTP 201 Created):**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "salary": 75000
}
```

### GET /customers

**Response (HTTP 200 OK):**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "salary": 75000
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "salary": 65000
  }
]
```

### GET /customers/1

**Response (HTTP 200 OK):**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "salary": 75000
}
```

### PUT /customers/1

**Request:**
```json
{
  "name": "Alice Johnson",
  "salary": 80000
}
```

**Response (HTTP 200 OK):**
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "salary": 80000
}
```

### DELETE /customers/1

**Response (HTTP 204 No Content)** — No body returned

---

## Customer Model

Each customer has the following attributes:

- **id** (integer): Unique identifier, auto-generated
- **name** (string): Customer's full name
- **salary** (float): Customer's salary

---

## Architecture Overview

This project follows a **clean layered architecture** pattern for maintainability and scalability:

### 1. **Customer Domain Model** (`customer.py`)
- Core business entity representing a customer
- Constructor with `id`, `name`, and `salary` parameters
- Getter methods: `get_id()`, `get_name()`, `get_salary()`
- Setter methods: `set_id()`, `set_name()`, `set_salary()`
- Helper method: `to_dict()` for serialization

### 2. **Pydantic Models** (`models.py`)
- `CustomerIn`: Validation schema for incoming requests (name, salary required)
- `CustomerOut`: Schema for API responses (id, name, salary)
- Automatic type validation and error handling

### 3. **Repository Layer** (`customer_repo.py`)
- Handles all data persistence operations
- In-memory dictionary storage with auto-incrementing IDs
- Methods: `create()`, `find_by_id()`, `find_all()`, `update()`, `delete()`

### 4. **Service Layer** (`customer_service.py`)
- Implements business logic and workflows
- Bridges domain objects and Pydantic models
- All CRUD operations here

### 5. **Controller Layer** (`customer_controller.py`)
- Defines all API routes and HTTP endpoints
- Each method includes comments with HTTP verb, endpoint path, full URL, and return type
- Handles request/response mapping and error handling with appropriate HTTP status codes
- Routes: POST, GET (all), GET (by id), PUT, DELETE

### 6. **Main Application** (`main.py`)
- Initializes FastAPI app instance
- Wires up repository → service → controller dependencies
- Registers customer router with all endpoints
- Includes health check endpoint
