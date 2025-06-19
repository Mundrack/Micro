"""
Book Controller Module

This module defines the HTTP endpoints for book-related operations.
Controllers handle HTTP requests, validate input data, delegate business
logic to services, and return appropriate HTTP responses.

The controller follows RESTful principles and provides comprehensive
CRUD operations for book management.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
import logging

# Import schemas for request/response validation
from app.schemas.book_schema import (
    BookCreate, 
    BookUpdate, 
    BookResponse, 
    BookListResponse,
    BookSearchQuery
)

# Import service interface for dependency injection
from app.services.book_service import BookService
from app.dependencies import get_book_service

# Configure module logger
logger = logging.getLogger(__name__)

# Create router instance for book endpoints
router = APIRouter()

@router.get("/books", response_model=BookListResponse, summary="Get all books")
async def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query"),
    author_id: Optional[str] = Query(None, description="Filter by author ID"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    available_only: bool = Query(False, description="Show only available books"),
    book_service: BookService = Depends(get_book_service)
) -> BookListResponse:
    """
    Retrieve a paginated list of books with optional filtering.
    
    This endpoint supports various query parameters for filtering and pagination:
    - Search by title, description, or tags
    - Filter by author or category
    - Show only available books
    - Paginate results
    
    Args:
        page (int): Page number (starts from 1)
        per_page (int): Number of items per page (max 100)
        search (str, optional): Search query string
        author_id (str, optional): Filter by specific author
        category_id (str, optional): Filter by specific category
        available_only (bool): Show only books with available copies
        book_service (BookService): Injected book service instance
    
    Returns:
        BookListResponse: Paginated list of books with metadata
    
    Raises:
        HTTPException: If validation fails or service error occurs
    """
    try:
        logger.info(f"Fetching books - Page: {page}, Per page: {per_page}")
        
        # Create search query object
        search_query = BookSearchQuery(
            query=search,
            author_id=author_id,
            category_id=category_id,
            available_only=available_only,
            page=page,
            per_page=per_page
        )
        
        # Delegate to service layer
        result = await book_service.get_books(search_query)
        
        logger.info(f"Successfully retrieved {len(result.books)} books")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error in get_books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching books"
        )

@router.get("/books/{book_id}", response_model=BookResponse, summary="Get book by ID")
async def get_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """
    Retrieve a specific book by its ID.
    
    Args:
        book_id (str): The unique identifier of the book
        book_service (BookService): Injected book service instance
    
    Returns:
        BookResponse: The requested book data
    
    Raises:
        HTTPException: If book not found or service error occurs
    """
    try:
        logger.info(f"Fetching book with ID: {book_id}")
        
        book = await book_service.get_book_by_id(book_id)
        
        if not book:
            logger.warning(f"Book not found: {book_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        logger.info(f"Successfully retrieved book: {book.title}")
        return book
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in get_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the book"
        )

@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="Create a new book")
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """
    Create a new book in the library system.
    
    This endpoint validates the input data, checks for duplicate ISBNs,
    verifies that referenced author and category exist, and creates the book.
    
    Args:
        book_data (BookCreate): The book data to create
        book_service (BookService): Injected book service instance
    
    Returns:
        BookResponse: The created book data with generated ID and timestamps
    
    Raises:
        HTTPException: If validation fails, duplicates exist, or service error occurs
    """
    try:
        logger.info(f"Creating new book: {book_data.title}")
        
        # Delegate to service layer for business logic and validation
        new_book = await book_service.create_book(book_data)
        
        logger.info(f"Successfully created book with ID: {new_book.id}")
        return new_book
        
    except ValueError as e:
        logger.error(f"Validation error in create_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the book"
        )

@router.put("/books/{book_id}", response_model=BookResponse, summary="Update a book")
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
) -> BookResponse:
    """
    Update an existing book with new data.
    
    This endpoint allows partial updates - only provided fields will be updated.
    It validates the data, checks constraints, and updates the book.
    
    Args:
        book_id (str): The unique identifier of the book to update
        book_data (BookUpdate): The updated book data
        book_service (BookService): Injected book service instance
    
    Returns:
        BookResponse: The updated book data
    
    Raises:
        HTTPException: If book not found, validation fails, or service error occurs
    """
    try:
        logger.info(f"Updating book with ID: {book_id}")
        
        # Delegate to service layer for business logic and validation
        updated_book = await book_service.update_book(book_id, book_data)
        
        if not updated_book:
            logger.warning(f"Book not found for update: {book_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        logger.info(f"Successfully updated book: {updated_book.title}")
        return updated_book
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in update_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in update_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the book"
        )

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book")
async def delete_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
) -> None:
    """
    Delete a book from the library system.
    
    This endpoint removes a book from the database. The operation is irreversible.
    Consider implementing soft delete for production systems.
    
    Args:
        book_id (str): The unique identifier of the book to delete
        book_service (BookService): Injected book service instance
    
    Returns:
        None: Returns 204 No Content on successful deletion
    
    Raises:
        HTTPException: If book not found or service error occurs
    """
    try:
        logger.info(f"Deleting book with ID: {book_id}")
        
        # Delegate to service layer
        success = await book_service.delete_book(book_id)
        
        if not success:
            logger.warning(f"Book not found for deletion: {book_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        logger.info(f"Successfully deleted book with ID: {book_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete_book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the book"
        )

@router.get("/books/{book_id}/availability", summary="Check book availability")
async def check_book_availability(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
) -> dict:
    """
    Check the availability status of a specific book.
    
    This endpoint provides detailed availability information including
    total copies, available copies, and lending status.
    
    Args:
        book_id (str): The unique identifier of the book
        book_service (BookService): Injected book service instance
    
    Returns:
        dict: Availability information
    
    Raises:
        HTTPException: If book not found or service error occurs
    """
    try:
        logger.info(f"Checking availability for book ID: {book_id}")
        
        availability = await book_service.check_availability(book_id)
        
        if availability is None:
            logger.warning(f"Book not found for availability check: {book_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        logger.info(f"Successfully checked availability for book: {book_id}")
        return availability
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in check_book_availability: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while checking book availability"
        )