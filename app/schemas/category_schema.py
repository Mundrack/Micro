"""
Category Schema Definitions

This module contains Pydantic schemas for category-related data validation
and serialization. These schemas define the structure for API requests
and responses for category management operations.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.category import CategoryStatus

class CategoryBase(BaseModel):
    """
    Base schema with common category fields.
    
    This schema contains fields that are common across different
    category-related operations (create, update, response).
    """
    name: str = Field(..., description="Category name", min_length=2, max_length=50)
    description: Optional[str] = Field(None, description="Category description", max_length=500)
    parent_id: Optional[str] = Field(None, description="Parent category ID for hierarchy")
    slug: str = Field(..., description="URL-friendly identifier", regex=r"^[a-z0-9-]+$")
    color: Optional[str] = Field(None, description="Hex color code", regex=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, description="Icon identifier", max_length=50)
    sort_order: int = Field(default=0, description="Display order for sorting")
    is_featured: bool = Field(default=False, description="Whether to feature this category")
    keywords: List[str] = Field(default_factory=list, description="Keywords for search")
    status: CategoryStatus = Field(default=CategoryStatus.ACTIVE, description="Category status")

class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.
    
    This schema is used when clients send POST requests to create
    new categories. It includes validation for required fields and format.
    """
    
    @validator('slug')
    def validate_slug(cls, v):
        """Validate and normalize slug format."""
        if not v:
            raise ValueError('Slug cannot be empty')
        
        # Convert to lowercase and replace spaces with hyphens
        slug = v.lower().replace(' ', '-')
        
        # Remove any characters that aren't letters, numbers, or hyphens
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        # Remove consecutive hyphens and leading/trailing hyphens
        slug = re.sub(r'-+', '-', slug).strip('-')
        
        if not slug:
            raise ValueError('Slug must contain at least one alphanumeric character')
        
        return slug
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "name": "Science Fiction",
                "description": "Books featuring futuristic concepts and technologies",
                "slug": "science-fiction",
                "color": "#3B82F6",
                "icon": "rocket",
                "sort_order": 10,
                "is_featured": True,
                "keywords": ["sci-fi", "future", "technology", "space"],
                "status": "active"
            }
        }

class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing category.
    
    This schema allows partial updates - all fields are optional.
    Only provided fields will be updated in the database.
    """
    name: Optional[str] = Field(None, description="Category name", min_length=2, max_length=50)
    description: Optional[str] = Field(None, description="Category description", max_length=500)
    parent_id: Optional[str] = Field(None, description="Parent category ID for hierarchy")
    slug: Optional[str] = Field(None, description="URL-friendly identifier", regex=r"^[a-z0-9-]+$")
    color: Optional[str] = Field(None, description="Hex color code", regex=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, description="Icon identifier", max_length=50)
    sort_order: Optional[int] = Field(None, description="Display order for sorting")
    is_featured: Optional[bool] = Field(None, description="Whether to feature this category")
    keywords: Optional[List[str]] = Field(None, description="Keywords for search")
    status: Optional[CategoryStatus] = Field(None, description="Category status")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "description": "Updated description for the category",
                "color": "#10B981",
                "is_featured": False
            }
        }

class CategoryResponse(CategoryBase):
    """
    Schema for category API responses.
    
    This schema includes all category data plus metadata like
    creation/update timestamps and computed fields.
    """
    id: str = Field(..., alias="_id", description="Category ID")
    book_count: int = Field(default=0, description="Number of books in this category")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Computed properties
    is_active: bool = Field(..., description="Whether the category is currently active")
    full_path: str = Field(..., description="Full hierarchical path")
    
    class Config:
        """Pydantic configuration."""
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "Science Fiction",
                "description": "Books featuring futuristic concepts",
                "parent_id": None,
                "slug": "science-fiction",
                "color": "#3B82F6",
                "icon": "rocket",
                "sort_order": 10,
                "is_featured": True,
                "keywords": ["sci-fi", "future", "technology"],
                "status": "active",
                "book_count": 150,
                "is_active": True,
                "full_path": "Science Fiction",
                "created_at": "2023-01-15T10:30:00Z",
                "updated_at": "2023-01-15T10:30:00Z"
            }
        }

class CategoryTreeResponse(BaseModel):
    """
    Schema for hierarchical category tree responses.
    
    This schema represents categories in a tree structure,
    showing parent-child relationships.
    """
    category: CategoryResponse = Field(..., description="The category data")
    children: List['CategoryTreeResponse'] = Field(default_factory=list, description="Child categories")
    depth: int = Field(default=0, description="Depth level in the hierarchy")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "category": {
                    "id": "507f1f77bcf86cd799439011",
                    "name": "Fiction",
                    "slug": "fiction",
                    "book_count": 500,
                    "is_active": True
                },
                "children": [
                    {
                        "category": {
                            "id": "507f1f77bcf86cd799439012",
                            "name": "Science Fiction",
                            "slug": "science-fiction",
                            "parent_id": "507f1f77bcf86cd799439011",
                            "book_count": 150
                        },
                        "children": [],
                        "depth": 1
                    }
                ],
                "depth": 0
            }
        }

# Forward reference resolution for recursive model
CategoryTreeResponse.model_rebuild()