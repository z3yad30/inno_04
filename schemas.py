"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, field_validator


class StudentBase(BaseModel):
    """Base schema for student data."""
    id: str = Field(..., min_length=1, description="Student ID")
    name: str = Field(..., min_length=1, max_length=100, description="Student name")
    age: int = Field(..., ge=1, le=120, description="Student age")

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        """Validate that age is a positive number."""
        if v < 1:
            raise ValueError("Age must be a positive number")
        return v


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating a student."""
    name: str = Field(None, min_length=1, max_length=100)
    age: int = Field(None, ge=1, le=120)

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        """Validate that age is a positive number."""
        if v is not None and v < 1:
            raise ValueError("Age must be a positive number")
        return v


class StudentResponse(StudentBase):
    """Schema for student response."""
    
    class Config:
        from_attributes = True
