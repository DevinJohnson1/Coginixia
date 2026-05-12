# ============================================================
# FastAPI "Hello World + Users API" — Beginner Friendly
# ============================================================
# Run with:  uvicorn main:app --reload
# Docs at:   http://127.0.0.1:8000/docs
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Create the FastAPI app instance ---
app = FastAPI(title="Hello World + Users API")

# ============================================================
# In-memory "database" — just a Python list.
# Data is lost every time the server restarts.
# ============================================================
users_db = []

# Auto-increment counter for user IDs
next_id = 1


# ============================================================
# Data model — defines what a User looks like.
# Pydantic validates the incoming JSON automatically.
# ============================================================
class UserIn(BaseModel):
    """Fields the client must send when creating a user."""
    name: str
    email: str


class UserOut(BaseModel):
    """Fields returned to the client (includes the auto-generated id)."""
    id: int
    name: str
    email: str


# ============================================================
# Route 1: GET /
# The simplest possible endpoint — just says Hello World.
# ============================================================
@app.get("/")
def hello_world():
    return {"message": "Hello World"}


# ============================================================
# Route 2: POST /users
# Accepts a JSON body, creates a new user, stores it in memory.
# ============================================================
@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    global next_id  # we modify the module-level counter

    # Build the new user dict with an auto-incremented id
    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
    }

    users_db.append(new_user)  # store in the in-memory list
    next_id += 1               # bump the counter for next time

    return new_user


# ============================================================
# Route 3: GET /users
# Returns the full list of users stored in memory.
# ============================================================
@app.get("/users", response_model=list[UserOut])
def list_users():
    return users_db
