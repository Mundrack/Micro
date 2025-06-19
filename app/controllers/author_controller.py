"""
Author Controller Module

This module defines the HTTP endpoints for author-related operations.
It provides comprehensive CRUD operations for author management,
including search, filtering, and relationship management.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
import logging

# Import schemas for request/response validation
from app.schemas.author_schema import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse
)

# Import service interface for dependency injection
from app.services.author_service import AuthorService
from app.dependencies import get_author_service

# Configure module logger
logger = logging.getLogger(__name__)

# Create router instance for author endpoints
router = APIRouter()

@router.get("/authors", response_model=List[AuthorResponse], summary="Get all authors")
async def get_authors(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or biography"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    status: Optional[str] = Query(None, description="Filter by status"),
    author_service: AuthorService = Depends(get_author_service)
) -> List[AuthorResponse]:
    """
    Retrieve a list of authors with optional filtering and pagination.
    
    Args:
        page (int): Page number for pagination
        per_page (int): Number of items per page
        search (str, optional): Search query for name or biography
        nationality (str, optional): Filter by author nationality
        status (str, optional): Filter by author status
        author_service (AuthorService): Injected author service instance
    
    Returns:
        List[AuthorResponse]: List of authors matching the criteria
    
    Raises:
        HTTPException: If validation fails or service error occurs
    """
    try:
        logger.info(f"Fetching authors - Page: {page}, Per page: {per_page}")
        
        authors = await author_service.get_authors(
            page=page,
            per_page=per_page,
            search=search,
            nationality=nationality,
            status=status
        )
        
        logger.info(f"Successfully retrieved {len(authors)} authors")
        return authors
        
    except Exception as e:
        logger.error(f"Error fetching authors: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching authors"
        )

@router.get("/authors/{author_id}", response_model=AuthorResponse, summary="Get author by ID")
async def get_author(
    author_id: str,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """
    Retrieve a specific author by their ID.
    
    Args:
        author_id (str): The unique identifier of the author
        author_service (AuthorService): Injected author service instance
    
    Returns:
        AuthorResponse: The requested author data
    
    Raises:
        HTTPException: If author not found or service error occurs
    """
    try:
        logger.info(f"Fetching author with ID: {author_id}")
        
        author = await author_service.get_author_by_id(author_id)
        
        if not author:
            logger.warning(f"Author not found: {author_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        
        logger.info(f"Successfully retrieved author: {author.name}")
        return author
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the author"
        )

@router.post("/authors", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED, summary="Create a new author")
async def create_author(
    author_data: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """
    Create a new author in the library system.
    
    Args:
        author_data (AuthorCreate): The author data to create
        author_service (AuthorService): Injected author service instance
    
    Returns:
        AuthorResponse: The created author data with generated ID
    
    Raises:
        HTTPException: If validation fails or service error occurs
    """
    try:
        logger.info(f"Creating new author: {author_data.name}")
        
        new_author = await author_service.create_author(author_data)
        
        logger.info(f"Successfully created author with ID: {new_author.id}")
        return new_author
        
    except ValueError as e:
        logger.error(f"Validation error in create_author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the author"
        )

@router.put("/authors/{author_id}", response_model=AuthorResponse, summary="Update an author")
async def update_author(
    author_id: str,
    author_data: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service)
) -> AuthorResponse:
    """
    Update an existing author with new data.
    
    Args:
        author_id (str): The unique identifier of the author to update
        author_data (AuthorUpdate): The updated author data
        author_service (AuthorService): Injected author service instance
    
    Returns:
        AuthorResponse: The updated author data
    
    Raises:
        HTTPException: If author not found or service error occurs
    """
    try:
        logger.info(f"Updating author with ID: {author_id}")
        
        updated_author = await author_service.update_author(author_id, author_data)
        
        if not updated_author:
            logger.warning(f"Author not found for update: {author_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        
        logger.info(f"Successfully updated author: {updated_author.name}")
        return updated_author
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in update_author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the author"
        )

@router.delete("/authors/{author_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an author")
async def delete_author(
    author_id: str,
    author_service: AuthorService = Depends(get_author_service)
) -> None:
    """
    Delete an author from the library system.
    
    Note: This operation will fail if the author has associated books.
    Consider implementing cascade deletion or soft delete for production.
    
    Args:
        author_id (str): The unique identifier of the author to delete
        author_service (AuthorService): Injected author service instance
    
    Returns:
        None: Returns 204 No Content on successful deletion
    
    Raises:
        HTTPException: If author not found, has dependencies, or service error occurs
    """
    try:
        logger.info(f"Deleting author with ID: {author_id}")
        
        success = await author_service.delete_author(author_id)
        
        if not success:
            logger.warning(f"Author not found for deletion: {author_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found"
            )
        
        logger.info(f"Successfully deleted author with ID: {author_id}")
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Cannot delete author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting author: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the author"
        )

@router.get("/authors/{author_id}/books", summary="Get books by author")
async def get_author_books(
    author_id: str,
    author_service: AuthorService = Depends(get_author_service)
) -> List[dict]:
    """
    Get all books written by a specific author.
    
    Args:
        author_id (str): The unique identifier of the author
        author_service (AuthorService): Injected author service instance
    
    Returns:
        List[dict]: List of books by the author
    
    Raises:
        HTTPException: If author not found or service error occurs
    """
    try:
        logger.info(f"Fetching books for author ID: {author_id}")
        
        books = await author_service.get_author_books(author_id)
        
        logger.info(f"Successfully retrieved {len(books)} books for author: {author_id}")
        return books
        
    except Exception as e:
        logger.error(f"Error fetching author books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching author's books"
        )