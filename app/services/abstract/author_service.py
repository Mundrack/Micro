"""
Author Service Interface

This module defines the abstract interface for author-related business operations.
It provides contracts for author management, relationship handling,
and business rule enforcement.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.schemas.author_schema import AuthorCreate, AuthorUpdate, AuthorResponse

class AuthorService(ABC):
    """
    Abstract base class defining the contract for author service operations.
    
    This interface ensures consistent author service implementations
    across different concrete classes.
    """

    @abstractmethod
    async def get_authors(
        self,
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        nationality: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[AuthorResponse]:
        """
        Retrieve authors with optional filtering and pagination.
        
        Args:
            page (int): Page number for pagination
            per_page (int): Number of items per page
            search (str, optional): Search query for name or biography
            nationality (str, optional): Filter by nationality
            status (str, optional): Filter by status
            
        Returns:
            List[AuthorResponse]: List of authors matching criteria
        """
        pass

    @abstractmethod
    async def get_author_by_id(self, author_id: str) -> Optional[AuthorResponse]:
        """
        Retrieve a specific author by ID.
        
        Args:
            author_id (str): The unique identifier of the author
            
        Returns:
            Optional[AuthorResponse]: The author data if found, None otherwise
        """
        pass

    @abstractmethod
    async def create_author(self, author_data: AuthorCreate) -> AuthorResponse:
        """
        Create a new author with validation.
        
        Args:
            author_data (AuthorCreate): The author data to create
            
        Returns:
            AuthorResponse: The created author data
            
        Raises:
            ValueError: If validation fails
        """
        pass

    @abstractmethod
    async def update_author(self, author_id: str, author_data: AuthorUpdate) -> Optional[AuthorResponse]:
        """
        Update an existing author.
        
        Args:
            author_id (str): The unique identifier of the author
            author_data (AuthorUpdate): The updated author data
            
        Returns:
            Optional[AuthorResponse]: Updated author data if successful, None if not found
            
        Raises:
            ValueError: If validation fails
        """
        pass

    @abstractmethod
    async def delete_author(self, author_id: str) -> bool:
        """
        Delete an author from the system.
        
        Args:
            author_id (str): The unique identifier of the author
            
        Returns:
            bool: True if deletion successful, False if not found
            
        Raises:
            ValueError: If author has associated books
        """
        pass

    @abstractmethod
    async def get_author_books(self, author_id: str) -> List[Dict[str, Any]]:
        """
        Get all books by a specific author.
        
        Args:
            author_id (str): The unique identifier of the author
            
        Returns:
            List[Dict[str, Any]]: List of books by the author
        """
        pass

    @abstractmethod
    async def update_book_count(self, author_id: str) -> None:
        """
        Update the book count for an author.
        
        This method recalculates and updates the number of books
        associated with an author.
        
        Args:
            author_id (str): The unique identifier of the author
        """
        pass