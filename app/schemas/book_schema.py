"""
Book Schema Definitions

This module contains Pydantic schemas for book-related data validation
and serialization. These schemas define the structure for API requests
and responses, ensuring data integrity and providing clear documentation.

The schemas separate input/output data structures from the database models,
allowing for flexible API design and validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic compatibility."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class BookBase(BaseModel):
    """
    Base schema with common book fields.
    
    This schema contains fields that are common across different
    book-related operations (create, update, response).
    """
    title: str = Field(..., description="Book title", min_length=1, max_length=200)
    isbn: str = Field(..., description="International Standard Book Number", 
                     regex=r"^(?:\d{9}[\dX]|\d{13})$")
    author_id: PyObjectId = Field(..., description="Reference to the author")
    category_id: PyObjectId = Field(..., description="Reference to the category")
    description: Optional[str] = Field(None, description="Book description", max_length=1000)
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    pages: Optional[int] = Field(None, ge=1, le=10000, description="Number of pages")
    language: Optional[str] = Field("English", description="Book language", max_length=50)
    publisher: Optional[str] = Field(None, description="Publisher name", max_length=100)
    available_copies: int = Field(default=1, ge=0, description="Available copies")
    total_copies: int = Field(default=1, ge=1, description="Total copies")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")

class BookCreate(BookBase):
    """
    Schema for creating a new book.
    
    This schema is used when clients send POST requests to create
    new books. It includes all required fields and optional metadata.
    """
    
    @validator('available_copies')
    def validate_available_copies(cls, v, values):
        """Ensure available copies don't exceed total copies."""
        total_copies = values.get('total_copies', 1)
        if v > total_copies:
            raise ValueError('Available copies cannot exceed total copies')
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "isbn": "9780743273565",
                "author_id": "507f1f77bcf86cd799439011",
                "category_id": "507f1f77bcf86cd799439012",
                "description": "A classic American novel set in the Jazz Age",
                "publication_date": "1925-04-10T00:00:00Z",
                "pages": 180,
                "language": "English",
                "publisher": "Scribner",
                "available_copies": 3,
                "total_copies": 5,
                "tags": ["classic", "american literature", "jazz age"]
            }
        }

class BookUpdate(BaseModel):
    """
    Schema for updating an existing book.
    
    This schema allows partial updates - all fields are optional.
    Only provided fields will be updated in the database.
    """
    title: Optional[str] = Field(None, description="Book title", min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, description="International Standard Book Number",
                               regex=r"^(?:\d{9}[\dX]|\d{13})$")
    author_id: Optional[PyObjectId] = Field(None, description="Reference to the author")
    category_id: Optional[PyObjectId] = Field(None, description="Reference to the category")
    description: Optional[str] = Field(None, description="Book description", max_length=1000)
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    pages: Optional[int] = Field(None, ge=1, le=10000, description="Number of pages")
    language: Optional[str] = Field(None, description="Book language", max_length=50)
    publisher: Optional[str] = Field(None, description="Publisher name", max_length=100)
    available_copies: Optional[int] = Field(None, ge=0, description="Available copies")
    total_copies: Optional[int] = Field(None, ge=1, description="Total copies")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    
    @validator('available_copies')
    def validate_available_copies(cls, v, values):
        """Ensure available copies don't exceed total copies."""
        total_copies = values.get('total_copies')
        if v is not None and total_copies is not None and v > total_copies:
            raise ValueError('Available copies cannot exceed total copies')
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "title": "Updated Book Title",
                "available_copies": 2,
                "tags": ["updated", "classic"]
            }
        }

class BookResponse(BookBase):
    """
    Schema for book API responses.
    
    This schema includes all book data plus metadata like
    creation/update timestamps and computed fields.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", description="Book ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Computed properties
    is_available: bool = Field(..., description="Whether the book is available for lending")
    
    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "The Great Gatsby",
                "isbn": "9780743273565",
                "author_id": "507f1f77bcf86cd799439012",
                "category_id": "507f1f77bcf86cd799439013",
                "description": "A classic American novel",
                "publication_date": "1925-04-10T00:00:00Z",
                "pages": 180,
                "language": "English",
                "publisher": "Scribner",
                "available_copies": 3,
                "total_copies": 5,
                "tags": ["classic", "american literature"],
                "created_at": "2023-01-15T10:30:00Z",
                "updated_at": "2023-01-15T10:30:00Z",
                "is_available": true
            }
        }

class BookListResponse(BaseModel):
    """
    Schema for paginated book list responses.
    
    This schema provides a structured response for list endpoints
    including pagination metadata and the actual book data.
    """
    books: List[BookResponse] = Field(..., description="List of books")
    total: int = Field(..., description="Total number of books")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "books": [
                    {
                        "id": "507f1f77bcf86cd799439011",
                        "title": "The Great Gatsby",
                        "isbn": "9780743273565",
                        "author_id": "507f1f77bcf86cd799439012",
                        "category_id": "507f1f77bcf86cd799439013",
                        "available_copies": 3,
                        "total_copies": 5,
                        "is_available": True,
                        "created_at": "2023-01-15T10:30:00Z",
                        "updated_at": "2023-01-15T10:30:00Z"
                    }
                ],
                "total": 100,
                "page": 1,
                "per_page": 10,
                "pages": 10,
                "has_next": True,
                "has_prev": False
            }
        }

class BookSearchQuery(BaseModel):
    """
    Schema for book search query parameters.
    
    This schema defines the structure for search requests,
    including filters, sorting, and pagination options.
    """
    query: Optional[str] = Field(None, description="Search query string")
    author_id: Optional[PyObjectId] = Field(None, description="Filter by author")
    category_id: Optional[PyObjectId] = Field(None, description="Filter by category")
    language: Optional[str] = Field(None, description="Filter by language")
    available_only: Optional[bool] = Field(False, description="Show only available books")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field("title", description="Sort field")
    sort_order: Optional[str] = Field("asc", regex="^(asc|desc)$", description="Sort order")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "query": "gatsby",
                "category_id": "507f1f77bcf86cd799439013",
                "available_only": True,
                "page": 1,
                "per_page": 10,
                "sort_by": "title",
                "sort_order": "asc"
            }
        }