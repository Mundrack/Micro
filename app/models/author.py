"""
Author Document Model

This module defines the Author document model using Beanie ODM.
It represents authors in the library system with comprehensive
biographical and contact information.

The Author model serves as a reference for book authorship and
provides detailed information about book creators.
"""

from beanie import Document, Indexed
from pydantic import Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class AuthorStatus(str, Enum):
    """
    Enumeration for author status in the system.
    
    ACTIVE: Author is actively publishing and available
    INACTIVE: Author is no longer active but books remain
    DECEASED: Author has passed away
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    DECEASED = "deceased"

class Author(Document):
    """
    Author document model for MongoDB collection.
    
    This class defines the structure for author documents, including
    personal information, contact details, and professional metadata.
    
    Attributes:
        name (str): Full name of the author (required, indexed)
        email (EmailStr): Contact email address (unique)
        biography (str): Author's biographical information
        birth_date (date): Author's date of birth
        death_date (date): Author's date of death (if applicable)
        nationality (str): Author's nationality
        website (str): Author's official website URL
        social_media (dict): Social media profiles
        genres (List[str]): Literary genres the author writes in
        awards (List[str]): Awards and recognitions received
        status (AuthorStatus): Current status of the author
        book_count (int): Number of books by this author in the system
        created_at (datetime): Document creation timestamp
        updated_at (datetime): Last modification timestamp
    """
    
    # Required fields
    name: Indexed(str) = Field(..., description="Author's full name", min_length=2, max_length=100)
    
    # Contact information
    email: Optional[EmailStr] = Field(None, description="Author's email address")
    
    # Biographical information
    biography: Optional[str] = Field(None, description="Author's biography", max_length=2000)
    birth_date: Optional[date] = Field(None, description="Date of birth")
    death_date: Optional[date] = Field(None, description="Date of death")
    nationality: Optional[str] = Field(None, description="Author's nationality", max_length=50)
    
    # Professional information
    website: Optional[str] = Field(None, description="Author's official website")
    social_media: Optional[dict] = Field(default_factory=dict, description="Social media profiles")
    genres: List[str] = Field(default_factory=list, description="Genres the author writes in")
    awards: List[str] = Field(default_factory=list, description="Awards and recognitions")
    
    # Status and metadata
    status: AuthorStatus = Field(default=AuthorStatus.ACTIVE, description="Author's current status")
    book_count: int = Field(default=0, ge=0, description="Number of books in the system")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    @validator('death_date')
    def validate_death_date(cls, v, values):
        """
        Validate that death date is after birth date.
        
        Args:
            v (date): Death date value
            values (dict): Other field values
            
        Returns:
            date: Validated death date
            
        Raises:
            ValueError: If death date is before birth date
        """
        birth_date = values.get('birth_date')
        if v and birth_date and v <= birth_date:
            raise ValueError('Death date must be after birth date')
        return v
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """
        Validate that birth date is not in the future.
        
        Args:
            v (date): Birth date value
            
        Returns:
            date: Validated birth date
            
        Raises:
            ValueError: If birth date is in the future
        """
        if v and v > date.today():
            raise ValueError('Birth date cannot be in the future')
        return v
    
    @validator('website')
    def validate_website(cls, v):
        """
        Validate website URL format.
        
        Args:
            v (str): Website URL
            
        Returns:
            str: Validated website URL
            
        Raises:
            ValueError: If URL format is invalid
        """
        if v and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('Website URL must start with http:// or https://')
        return v
    
    @validator('social_media')
    def validate_social_media(cls, v):
        """
        Validate social media profiles format.
        
        Args:
            v (dict): Social media profiles dictionary
            
        Returns:
            dict: Validated social media profiles
        """
        if not v:
            return {}
        
        allowed_platforms = ['twitter', 'facebook', 'instagram', 'linkedin', 'goodreads']
        validated = {}
        
        for platform, profile in v.items():
            if platform.lower() in allowed_platforms:
                validated[platform.lower()] = profile
        
        return validated
    
    def get_age(self) -> Optional[int]:
        """
        Calculate author's current age or age at death.
        
        Returns:
            Optional[int]: Age in years, None if birth date is unknown
        """
        if not self.birth_date:
            return None
        
        end_date = self.death_date or date.today()
        age = end_date.year - self.birth_date.year
        
        # Adjust for birthday not yet reached this year
        if end_date.month < self.birth_date.month or \
           (end_date.month == self.birth_date.month and end_date.day < self.birth_date.day):
            age -= 1
        
        return age
    
    def is_active(self) -> bool:
        """
        Check if the author is currently active.
        
        Returns:
            bool: True if author status is ACTIVE, False otherwise
        """
        return self.status == AuthorStatus.ACTIVE
    
    def add_genre(self, genre: str) -> None:
        """
        Add a genre to the author's genre list.
        
        Args:
            genre (str): Genre to add
        """
        if genre and genre not in self.genres:
            self.genres.append(genre)
    
    def add_award(self, award: str) -> None:
        """
        Add an award to the author's awards list.
        
        Args:
            award (str): Award to add
        """
        if award and award not in self.awards:
            self.awards.append(award)
    
    class Settings:
        """Beanie document settings."""
        name = "authors"  # MongoDB collection name
        indexes = [
            "name",
            "email",
            "nationality",
            "status",
            "genres",
            [("name", "text"), ("biography", "text")]  # Text search index
        ]