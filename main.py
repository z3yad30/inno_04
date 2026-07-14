"""FastAPI application for Student Management System."""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db, init_db, Student
from schemas import StudentCreate, StudentUpdate, StudentResponse

app = FastAPI(
    title="Student Management API",
    description="A REST API for managing students",
    version="1.0.0"
)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Add a new student to the database.
    
    - **id**: Unique student identifier
    - **name**: Student's full name
    - **age**: Student's age (must be positive)
    """
    # Check if student with this ID already exists
    existing_student = db.query(Student).filter(Student.id == student.id).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with ID {student.id} already exists"
        )
    
    db_student = Student(id=student.id, name=student.name, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    """
    Retrieve a list of all students.
    """
    students = db.query(Student).all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    """
    Fetch a specific student's details by ID.
    
    - **student_id**: The ID of the student to retrieve
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: str, student_update: StudentUpdate, db: Session = Depends(get_db)):
    """
    Update an existing student's information.
    
    - **student_id**: The ID of the student to update
    - **name**: New name (optional)
    - **age**: New age (optional)
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    if student_update.name is not None:
        student.name = student_update.name
    if student_update.age is not None:
        student.age = student_update.age
    
    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """
    Remove a student from the database.
    
    - **student_id**: The ID of the student to delete
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    db.delete(student)
    db.commit()
    return None


@app.get("/")
def read_root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Student Management API",
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }
