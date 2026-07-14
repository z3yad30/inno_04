# Student Management API

A RESTful API for managing students built with FastAPI and SQLite.

## Evolution from Task 04

This is the upgraded version of the Student Management System. Instead of a command-line interface with JSON storage, this implementation provides:

- **RESTful API**: HTTP-based endpoints for CRUD operations
- **SQLite Database**: Persistent relational database storage (students.db)
- **Data Validation**: Strict input validation using Pydantic schemas
- **HTTP Status Codes**: Proper response codes for different scenarios
- **Interactive Documentation**: Auto-generated API docs via Swagger UI

## Features

✨ Core Functionality:
- ➕ Add new students via POST requests
- 📋 Retrieve all students or search by ID
- ✏️ Update student information
- 🗑️ Delete students from the database
- ⚙️ Automatic database initialization on startup
- 📚 Interactive API documentation

## Project Structure

```
task_04/
├── main.py              # FastAPI application with all endpoints
├── database.py          # SQLAlchemy models and database setup
├── schemas.py           # Pydantic schemas for validation
├── student_manager.py   # Original CLI implementation (for reference)
├── students.json        # Original JSON data (for reference)
├── students.db          # SQLite database (created automatically)
├── requirements.txt     # Python dependencies
└── tests/
    ├── test_student_manager.py  # Tests for original CLI
    └── test_api.py              # Tests for FastAPI endpoints
```

## Installation

1. **Create and activate virtual environment** (if not already done):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the API

**Start the server**:
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Swagger UI (Interactive Docs)**: `http://localhost:8000/docs`
- **ReDoc (Alternative Docs)**: `http://localhost:8000/redoc`

## API Endpoints

### 1. **POST /students** - Create a New Student
**Status Code**: 201 Created

**Request Body**:
```json
{
  "id": "S001",
  "name": "John Doe",
  "age": 20
}
```

**Response**:
```json
{
  "id": "S001",
  "name": "John Doe",
  "age": 20
}
```

**Error Cases**:
- `409 Conflict`: If a student with the same ID already exists
- `422 Unprocessable Entity`: If validation fails (invalid age, missing fields)

---

### 2. **GET /students** - Get All Students
**Status Code**: 200 OK

**Response**:
```json
[
  {
    "id": "S001",
    "name": "John Doe",
    "age": 20
  },
  {
    "id": "S002",
    "name": "Jane Smith",
    "age": 21
  }
]
```

---

### 3. **GET /students/{id}** - Get a Specific Student
**Status Code**: 200 OK (if found) or 404 Not Found

**Example**: `GET /students/S001`

**Response** (200):
```json
{
  "id": "S001",
  "name": "John Doe",
  "age": 20
}
```

**Response** (404):
```json
{
  "detail": "Student with ID S001 not found"
}
```

---

### 4. **PUT /students/{id}** - Update a Student
**Status Code**: 200 OK or 404 Not Found

**Example**: `PUT /students/S001`

**Request Body** (both fields optional):
```json
{
  "name": "John D. Doe",
  "age": 21
}
```

**Response**:
```json
{
  "id": "S001",
  "name": "John D. Doe",
  "age": 21
}
```

**Error Cases**:
- `404 Not Found`: If student doesn't exist
- `422 Unprocessable Entity`: If validation fails

---

### 5. **DELETE /students/{id}** - Delete a Student
**Status Code**: 204 No Content (if successful) or 404 Not Found

**Example**: `DELETE /students/S001`

**Response** (204): Empty body

**Response** (404):
```json
{
  "detail": "Student with ID S001 not found"
}
```

---

## Running Tests

### Run API Tests:
```bash
pytest tests/test_api.py -v
```

### Run Original CLI Tests:
```bash
pytest tests/test_student_manager.py -v
```

### Run All Tests:
```bash
pytest tests/ -v
```

### Test Coverage Report:
```bash
pytest tests/ --cov=. --cov-report=html
```

## Data Validation Rules

- **ID**: Required, non-empty string
- **Name**: Required, 1-100 characters
- **Age**: Required, positive integer (1-120)

Validation errors return a 422 status code with details about the invalid fields.

## Example Usage with curl

```bash
# Create a student
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{"id":"S001","name":"Alice","age":20}'

# Get all students
curl -X GET "http://localhost:8000/students"

# Get a specific student
curl -X GET "http://localhost:8000/students/S001"

# Update a student
curl -X PUT "http://localhost:8000/students/S001" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Smith","age":21}'

# Delete a student
curl -X DELETE "http://localhost:8000/students/S001"
```

## Example Usage with Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a student
response = requests.post(
    f"{BASE_URL}/students",
    json={"id": "S001", "name": "Bob", "age": 22}
)
print(response.status_code)  # 201

# Get all students
response = requests.get(f"{BASE_URL}/students")
print(response.json())

# Update a student
response = requests.put(
    f"{BASE_URL}/students/S001",
    json={"age": 23}
)
print(response.json())

# Delete a student
response = requests.delete(f"{BASE_URL}/students/S001")
print(response.status_code)  # 204
```

## Technical Stack

- **Framework**: FastAPI - Modern, fast web framework with automatic API documentation
- **Database**: SQLite - Lightweight relational database
- **ORM**: SQLAlchemy - SQL toolkit and Object-Relational Mapping
- **Validation**: Pydantic - Data validation using Python type annotations
- **Server**: Uvicorn - ASGI server for running FastAPI
- **Testing**: Pytest - Testing framework with TestClient for API testing

## Key Improvements Over Task 04

| Feature | Task 04 (CLI) | Task 05 (API) |
|---------|---------------|----------------|
| Interface | Command-line menu | HTTP REST endpoints |
| Storage | JSON file (students.json) | SQLite database (students.db) |
| Concurrency | Single user | Multiple concurrent users |
| Validation | Basic string validation | Strict Pydantic validation |
| Error Handling | Custom error messages | HTTP status codes |
| Documentation | None | Auto-generated Swagger UI |
| Scalability | Limited | Production-ready |
| Integration | Hard to integrate | Easy API integration |

## Architecture Overview

```
Client (Browser, curl, Python requests, etc.)
    ↓
FastAPI Application (main.py)
    ├── Pydantic Schemas (schemas.py) - Request/Response validation
    └── SQLAlchemy ORM (database.py) - Database abstraction
        └── SQLite Database (students.db)
```

## Future Enhancements

- Add authentication (JWT tokens)
- Add pagination for GET /students
- Add filtering and sorting capabilities
- Add rate limiting
- Add database migrations with Alembic
- Add logging
- Deploy to cloud (Heroku, AWS, etc.)

## Running the Original CLI (Task 04)

If you want to run the original command-line version:
```bash
python student_manager.py
```

Note: The CLI version saves data to `students.json`, while the API version uses `students.db`. They do not share data.
