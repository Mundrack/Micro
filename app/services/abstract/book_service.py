"""
Book Service Interface

This module defines the abstract interface for book-related business operations.
It follows the Dependency Inversion Principle by defining contracts that
implementations must follow, enabling easy testing and flexibility.

The interface defines all business operations for book management,
including CRUD operations, search, validation, and business rules.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.schemas.book_schema import (
    BookCreate, 
    BookUpdate, 
    BookResponse, 
    BookListResponse,
    BookSearchQuery
)

class BookService(ABC):
    """
    Abstract base class defining the contract for book service operations.
    
    This interface ensures that all book service implementations
    provide the same set of operations with consistent signatures.
    """

    @abstractmethod
    async def get_books(self, search_query: BookSearchQuery) -> BookListResponse:
        """
        Retrieve books with filtering, searching, and pagination.
        
        Args:
            search_query (BookSearchQuery): Search and filter parameters
            
        Returns:
            BookListResponse: Paginated list of books with metadata
        """
        pass

    @abstractmethod
    async def get_book_by_id(self, book_id: str) -> Optional[BookResponse]:
        """
        Retrieve a specific book by its ID.
        
        Args:
            book_id (str): The unique identifier of the book
            
        Returns:
            Optional[BookResponse]: The book data if found, None otherwise
        """
        pass

    @abstractmethod
    async def create_book(self, book_data: BookCreate) -> BookResponse:
        """
        Create a new book with validation and business rules.
        
        This method should:
        - Validate input data
        - Check for duplicate ISBNs
        - Verify author and category exist
        - Apply business rules
        - Create the book in the database
        
        Args:
            book_data (BookCreate): The book data to create
            
        Returns:
            BookResponse: The created book data
            
        Raises:
            ValueError: If validation fails or business rules are violated
        """
        pass

    @abstractmethod
    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[BookResponse]:
        """
        Update an existing book with new data.
        
        This method should:
        - Validate input data
        - Check book exists
        - Verify any referenced entities exist
        - Apply business rules
        - Update the book in the database
        
        Args:
            book_id (str): The unique identifier of the book to update
            book_data (BookUpdate): The updated book data
            
        Returns:
            Optional[BookResponse]: The updated book data if successful, None if not found
            
        Raises:
            ValueError: If validation fails or business rules are violated
        """
        pass

    @abstractmethod
    async def delete_book(self, book_id: str) -> bool:
        """
        Delete a book from the system.
        
        This method should:
        - Check if book exists
        - Verify book can be safely deleted (no active loans, etc.)
        - Remove the book from the database
        
        Args:
            book_id (str): The unique identifier of the book to delete
            
        Returns:
            bool: True if deletion was successful, False if book not found
            
        Raises:
            ValueError: If book cannot be deleted due to business constraints
        """
        pass

    @abstractmethod
    async def check_availability(self, book_id: str) -> Optional[Dict[str, Any]]:
        """
        Check the availability status of a book.
        
        Args:
            book_id (str): The unique identifier of the book
            
        Returns:
            Optional[Dict[str, Any]]: Availability information if book exists, None otherwise
        """
        pass

    @abstractmethod
    async def search_books(self, query: str, limit: int = 10) -> List[BookResponse]:
        """
        Search books by title, description, or tags.
        
        Args:
            query (str): The search query string
            limit (int): Maximum number of results to return
            
        Returns:
            List[BookResponse]: List of matching books
        """
        pass

    @abstractmethod
    async def get_books_by_author(self, author_id: str) -> List[BookResponse]:
        """
        Get all books by a specific author.
        
        Args:
            author_id (str): The unique identifier of the author
            
        Returns:
            List[BookResponse]: List of books by the author
        """
        pass

    @abstractmethod
    async def get_books_by_category(self, category_id: str) -> List[BookResponse]:
        """
        Get all books in a specific category.
        
        Args:
            category_id (str): The unique identifier of the category
            
        Returns:
            List[BookResponse]: List of books in the category
        """
        pass

    @abstractmethod
    async def update_inventory(self, book_id: str, available_copies: int, total_copies: int) -> Optional[BookResponse]:
        """
        Update book inventory information.
        
        This method handles inventory management for library operations
        like lending and returning books.
        
        Args:
            book_id (str): The unique identifier of the book
            available_copies (int): New number of available copies
            total_copies (int): New total number of copies
            
        Returns:
            Optional[BookResponse]: Updated book data if successful, None if not found
            
        Raises:
            ValueError: If inventory values are invalid
        """
        pass