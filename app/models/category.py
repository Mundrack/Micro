"""
Category Document Model

This module defines the Category document model using Beanie ODM.
It represents book categories/genres in the library system with
hierarchical structure support and metadata management.

Categories help organize books and enable efficient browsing and filtering.
"""

from beanie import Document, Indexed
from pydantic import Field, validator
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from enum import Enum

class CategoryStatus(str, Enum):
    """
    Enumeration for category status in the system.
    
    ACTIVE: Category is active and can be assigned to books
    INACTIVE: Category is inactive but existing assignments remain
    DEPRECATED: Category is deprecated and should not be used
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"

class Category(Document):
    """
    Category document model for MongoDB collection.
    
    This class defines the structure for book categories, supporting
    hierarchical organization and comprehensive metadata.
    
    Attributes:
        name (str): Category name (required, indexed, unique)
        description (str): Detailed description of the category
        parent_id (ObjectId): Reference to parent category (for hierarchy)
        slug (str): URL-friendly identifier
        color (str): Hex color code for UI representation
        icon (str): Icon identifier for UI representation
        sort_order (int): Display order for category listing
        is_featured (bool): Whether category should be featured
        keywords (List[str]): Keywords for search and filtering
        book_count (int): Number of books in this category
        status (CategoryStatus): Current status of the category
        created_at (datetime): Document creation timestamp
        updated_at (datetime): Last modification timestamp
    """
    
    # Required fields
    name: Indexed(str) = Field(..., description="Category name", min_length=2, max_length=50)
    
    # Descriptive fields
    description: Optional[str] = Field(None, description="Category description", max_length=500)
    
    # Hierarchical structure
    parent_id: Optional[ObjectId] = Field(None, description="Parent category ID for hierarchy")
    
    # UI and display properties
    slug: Indexed(str) = Field(..., description="URL-friendly identifier", regex=r"^[a-z0-9-]+$")
    color: Optional[str] = Field(None, description="Hex color code", regex=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, description="Icon identifier", max_length=50)
    sort_order: int = Field(default=0, description="Display order for sorting")
    
    # Feature flags
    is_featured: bool = Field(default=False, description="Whether to feature this category")
    
    # Search and metadata
    keywords: List[str] = Field(default_factory=list, description="Keywords for search")
    book_count: int = Field(default=0, ge=0, description="Number of books in category")
    
    # Status management
    status: CategoryStatus = Field(default=CategoryStatus.ACTIVE, description="Category status")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('slug')
    def validate_slug(cls, v):
        """
        Validate and normalize slug format.
        
        Args:
            v (str): Slug value to validate
            
        Returns:
            str: Validated and normalized slug
            
        Raises:
            ValueError: If slug format is invalid
        """
        if not v:
            raise ValueError('Slug cannot be empty')
        
        # Convert to lowercase and replace spaces with hyphens
        slug = v.lower().replace(' ', '-')
        
        # Remove any characters that aren't letters, numbers, or hyphens
        import re
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        
        # Remove consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        if not slug:
            raise ValueError('Slug must contain at least one alphanumeric character')
        
        return slug
    
    @validator('name')
    def validate_name(cls, v):
        """
        Validate and normalize category name.
        
        Args:
            v (str): Name value to validate
            
        Returns:
            str: Validated and normalized name
        """
        if not v or not v.strip():
            raise ValueError('Category name cannot be empty')
        
        # Normalize whitespace
        return ' '.join(v.strip().split())
    
    @validator('keywords')
    def validate_keywords(cls, v):
        """
        Validate and normalize keywords list.
        
        Args:
            v (List[str]): Keywords list to validate
            
        Returns:
            List[str]: Validated and normalized keywords
        """
        if not v:
            return []
        
        # Remove duplicates and empty strings, normalize case
        normalized = []
        seen = set()
        
        for keyword in v:
            if isinstance(keyword, str) and keyword.strip():
                normalized_keyword = keyword.strip().lower()
                if normalized_keyword not in seen:
                    normalized.append(normalized_keyword)
                    seen.add(normalized_keyword)
        
        return normalized
    
    def is_active(self) -> bool:
        """
        Check if the category is currently active.
        
        Returns:
            bool: True if category status is ACTIVE, False otherwise
        """
        return self.status == CategoryStatus.ACTIVE
    
    def can_be_assigned(self) -> bool:
        """
        Check if the category can be assigned to books.
        
        Returns:
            bool: True if category is active, False otherwise
        """
        return self.status == CategoryStatus.ACTIVE
    
    def add_keyword(self, keyword: str) -> None:
        """
        Add a keyword to the category's keyword list.
        
        Args:
            keyword (str): Keyword to add
        """
        if keyword and keyword.strip():
            normalized = keyword.strip().lower()
            if normalized not in self.keywords:
                self.keywords.append(normalized)
    
    def get_full_path(self) -> str:
        """
        Get the full hierarchical path of the category.
        Note: This would need to be implemented with database queries
        to traverse the parent hierarchy.
        
        Returns:
            str: Full category path (e.g., "Fiction > Science Fiction > Cyberpunk")
        """
        # This is a placeholder - actual implementation would require
        # traversing the parent hierarchy through database queries
        return self.name
    
    class Settings:
        """Beanie document settings."""
        name = "categories"  # MongoDB collection name
        indexes = [
            "name",
            "slug",
            "parent_id",
            "status",
            "is_featured",
            "sort_order",
            "keywords",
            [("name", "text"), ("description", "text"), ("keywords", "text")]  # Text search
        ]