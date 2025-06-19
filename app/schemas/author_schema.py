"""
Author Schema Definitions

This module contains Pydantic schemas for author-related data validation
and serialization. These schemas define the structure for API requests
and responses for author management operations.
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
from app.models.author import AuthorStatus

class AuthorBase(BaseModel):
    """
    Base schema with common author fields.
    
    This schema contains fields that are common across different
    author-related operations (create, update, response).
    """
    name: str = Field(..., description="Author's full name", min_length=2, max_length=100)
    email: Optional[EmailStr] = Field(None, description="Author's email address")
    biography: Optional[str] = Field(None, description="Author's biography", max_length=2000)
    birth_date: Optional[date] = Field(None, description="Date of birth")
    death_date: Optional[date] = Field(None, description="Date of death")
    nationality: Optional[str] = Field(None, description="Author's nationality", max_length=50)
    website: Optional[str] = Field(None, description="Author's official website")
    social_media: Optional[dict] = Field(default_factory=dict, description="Social media profiles")
    genres: List[str] = Field(default_factory=list, description="Genres the author writes in")
    awards: List[str] = Field(default_factory=list, description="Awards and recognitions")
    status: AuthorStatus = Field(default=AuthorStatus.ACTIVE, description="Author's current status")

class AuthorCreate(AuthorBase):
    """
    Schema for creating a new author.
    
    This schema is used when clients send POST requests to create
    new authors. It includes validation for required fields and relationships.
    """
    
    @validator('death_date')
    def validate_death_date(cls, v, values):
        """Validate that death date is after birth date."""
        birth_date = values.get('birth_date')
        if v and birth_date and v <= birth_date:
            raise ValueError('Death date must be after birth date')
        return v
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Validate that birth date is not in the future."""
        if v and v > date.today():
            raise ValueError('Birth date cannot be in the future')
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "name": "F. Scott Fitzgerald",
                "email": "contact@fscottfitzgerald.com",
                "biography": "American novelist and short story writer",
                "birth_date": "1896-09-24",
                "death_date": "1940-12-21",
                "nationality": "American",
                "website": "https://www.fscottfitzgerald.com",
                "social_media": {
                    "goodreads": "fscottfitzgerald",
                    "twitter": "fscottfitz"
                },
                "genres": ["Literary Fiction", "Modernist Literature"],
                "awards": ["Posthumous Recognition"],
                "status": "deceased"
            }
        }

class AuthorUpdate(BaseModel):
    """
    Schema for updating an existing author.
    
    This schema allows partial updates - all fields are optional.
    Only provided fields will be updated in the database.
    """
    name: Optional[str] = Field(None, description="Author's full name", min_length=2, max_length=100)
    email: Optional[EmailStr] = Field(None, description="Author's email address")
    biography: Optional[str] = Field(None, description="Author's biography", max_length=2000)
    birth_date: Optional[date] = Field(None, description="Date of birth")
    death_date: Optional[date] = Field(None, description="Date of death")
    nationality: Optional[str] = Field(None, description="Author's nationality", max_length=50)
    website: Optional[str] = Field(None, description="Author's official website")
    social_media: Optional[dict] = Field(None, description="Social media profiles")
    genres: Optional[List[str]] = Field(None, description="Genres the author writes in")
    awards: Optional[List[str]] = Field(None, description="Awards and recognitions")
    status: Optional[AuthorStatus] = Field(None, description="Author's current status")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "biography": "Updated biography with new information",
                "website": "https://www.newwebsite.com",
                "awards": ["New Award", "Another Recognition"]
            }
        }

class AuthorResponse(AuthorBase):
    """
    Schema for author API responses.
    
    This schema includes all author data plus metadata like
    creation/update timestamps and computed fields.
    """
    id: str = Field(..., alias="_id", description="Author ID")
    book_count: int = Field(default=0, description="Number of books by this author")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Computed properties
    age: Optional[int] = Field(None, description="Author's current age or age at death")
    is_active: bool = Field(..., description="Whether the author is currently active")
    
    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "F. Scott Fitzgerald",
                "email": "contact@fscottfitzgerald.com",
                "biography": "American novelist and short story writer",
                "birth_date": "1896-09-24",
                "death_date": "1940-12-21",
                "nationality": "American",
                "genres": ["Literary Fiction"],
                "awards": ["Posthumous Recognition"],
                "status": "deceased",
                "book_count": 5,
                "age": 44,
                "is_active": False,
                "created_at": "2023-01-15T10:30:00Z",
                "updated_at": "2023-01-15T10:30:00Z"
            }
        }