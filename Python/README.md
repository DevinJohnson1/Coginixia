# Hello World + Users API — FastAPI Beginner Project

A minimal REST API built with FastAPI for learning purposes.  
Everything lives in a **single file** (`main.py`) with no real database.

---

## Project Structure

```
Python/
├── main.py           # The entire application
└── requirements.txt  # Python dependencies
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
| App root           | http://127.0.0.1:8000        |
| Interactive Swagger UI | http://127.0.0.1:8000/docs |
| Alternative ReDoc  | http://127.0.0.1:8000/redoc  |

The `--reload` flag makes the server restart automatically whenever you save `main.py` — great for development.

---

## API Endpoints

| Method | Path     | Description        |
|--------|----------|--------------------|
| GET    | `/`      | Hello World        |
| POST   | `/users` | Create a new user  |
| GET    | `/users` | List all users     |

---

## Sample curl Commands

### Hello World
```bash
curl http://127.0.0.1:8000/
```

### Create a user (POST /users)
```bash
curl -X POST http://127.0.0.1:8000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "email": "alice@example.com"}'
```

**Windows PowerShell equivalent:**
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/users `
  -ContentType "application/json" `
  -Body '{"name": "Alice", "email": "alice@example.com"}'
```

### List all users (GET /users)
```bash
curl http://127.0.0.1:8000/users
```

---

## Example Request & Response

### POST /users

**Request JSON**
```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Response JSON** (HTTP 201 Created)
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### GET /users

**Response JSON** (HTTP 200 OK)
```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  }
]
```

---

## How It Works — Plain English

### How does POST /users work?
1. Your HTTP client sends a JSON body (`name` + `email`) to `/users`.
2. FastAPI reads the JSON and validates it against the `UserIn` model (powered by Pydantic).  
   If a required field is missing or the wrong type, FastAPI automatically returns a `422 Unprocessable Entity` error — no extra code needed.
3. The code assigns the next available `id`, builds a dict, and appends it to `users_db` (a plain Python list).
4. The new user dict is returned as JSON with HTTP status `201 Created`.

### Where is the data stored?
In a **Python list in memory** (`users_db = []` in `main.py`).  
There is no file, no database, no disk — the list lives only while the server process is running.

### Why is this NOT production-ready?

| Problem | Reason |
|---------|--------|
| **No persistence** | All data is lost when the server restarts. |
| **No real database** | A real app would use PostgreSQL, MySQL, SQLite, etc. |
| **No authentication** | Anyone can create or read users. |
| **No input validation beyond types** | Email format is not verified. |
| **No duplicate checking** | You can add the same email twice. |
| **Single process / no concurrency safety** | The `next_id` counter would break under multiple workers. |

This project is intentionally simple so you can focus on **how FastAPI works** before adding those layers.
