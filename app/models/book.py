"""
Book Document Model

This module defines the Book document model using Beanie ODM.
It represents the book collection in MongoDB with all necessary
fields and validation rules.

The Book model includes relationships with Author and Category models
and provides the database schema for book-related operations.
"""

from beanie import Document, Indexed
from pydantic import Field, validator
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class Book(Document):
    """
    Book document model for MongoDB collection.
    
    This class defines the structure and validation rules for book documents
    stored in the MongoDB database. It inherits from Beanie's Document class
    to provide ODM functionality.
    
    Attributes:
        title (str): The book's title (required, indexed for search)
        isbn (str): International Standard Book Number (unique identifier)
        author_id (ObjectId): Reference to the author document
        category_id (ObjectId): Reference to the category document
        description (str): Detailed description of the book
        publication_date (datetime): When the book was published
        pages (int): Number of pages in the book
        language (str): Language of the book content
        publisher (str): Publishing company name
        available_copies (int): Number of copies available for lending
        total_copies (int): Total number of copies owned
        tags (List[str]): List of tags for categorization and search
        created_at (datetime): Document creation timestamp
        updated_at (datetime): Last modification timestamp
    """
    
    # Required fields
    title: Indexed(str) = Field(..., description="Book title", min_length=1, max_length=200)
    isbn: Indexed(str) = Field(..., description="International Standard Book Number", regex=r"^(?:\d{9}[\dX]|\d{13})$")
    
    # Foreign key references
    author_id: ObjectId = Field(..., description="Reference to the author")
    category_id: ObjectId = Field(..., description="Reference to the category")
    
    # Optional descriptive fields
    description: Optional[str] = Field(None, description="Book description", max_length=1000)
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    pages: Optional[int] = Field(None, ge=1, le=10000, description="Number of pages")
    language: Optional[str] = Field("English", description="Book language", max_length=50)
    publisher: Optional[str] = Field(None, description="Publisher name", max_length=100)
    
    # Inventory management
    available_copies: int = Field(default=1, ge=0, description="Available copies for lending")
    total_copies: int = Field(default=1, ge=1, description="Total copies owned")
    
    # Additional metadata
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    
    # Timestamps (automatically managed)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('available_copies')
    def validate_available_copies(cls, v, values):
        """
        Validate that available copies don't exceed total copies.
        
        Args:
            v (int): Available copies value
            values (dict): Other field values
            
        Returns:
            int: Validated available copies value
            
        Raises:
            ValueError: If available copies exceed total copies
        """
        total_copies = values.get('total_copies', 1)
        if v > total_copies:
            raise ValueError('Available copies cannot exceed total copies')
        return v
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """
        Validate ISBN format and check digit.
        
        Args:
            v (str): ISBN value to validate
            
        Returns:
            str: Validated ISBN
            
        Raises:
            ValueError: If ISBN format is invalid
        """
        # Remove any hyphens or spaces
        isbn = v.replace('-', '').replace(' ', '')
        
        if len(isbn) == 10:
            # Validate ISBN-10
            if not cls._validate_isbn10(isbn):
                raise ValueError('Invalid ISBN-10 check digit')
        elif len(isbn) == 13:
            # Validate ISBN-13
            if not cls._validate_isbn13(isbn):
                raise ValueError('Invalid ISBN-13 check digit')
        else:
            raise ValueError('ISBN must be 10 or 13 digits')
        
        return isbn
    
    @staticmethod
    def _validate_isbn10(isbn: str) -> bool:
        """Validate ISBN-10 check digit."""
        try:
            check_sum = sum((i + 1) * (int(char) if char != 'X' else 10) 
                          for i, char in enumerate(isbn))
            return check_sum % 11 == 0
        except ValueError:
            return False
    
    @staticmethod
    def _validate_isbn13(isbn: str) -> bool:
        """Validate ISBN-13 check digit."""
        try:
            check_sum = sum(int(char) * (1 if i % 2 == 0 else 3) 
                          for i, char in enumerate(isbn[:-1]))
            return (10 - (check_sum % 10)) % 10 == int(isbn[-1])
        except ValueError:
            return False
    
    def is_available(self) -> bool:
        """
        Check if the book is available for lending.
        
        Returns:
            bool: True if copies are available, False otherwise
        """
        return self.available_copies > 0
    
    def can_lend(self, quantity: int = 1) -> bool:
        """
        Check if a specific quantity can be lended.
        
        Args:
            quantity (int): Number of copies requested
            
        Returns:
            bool: True if quantity is available, False otherwise
        """
        return self.available_copies >= quantity
    
    class Settings:
        """Beanie document settings."""
        name = "books"  # MongoDB collection name
        indexes = [
            "title",
            "isbn",
            "author_id",
            "category_id",
            "tags",
            [("title", "text"), ("description", "text")]  # Text search index
        ]