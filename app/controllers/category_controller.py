"""
Category Controller Module

This module defines the HTTP endpoints for category-related operations.
It provides CRUD operations for category management with support for
hierarchical organization and tree structure operations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
import logging

# Import schemas for request/response validation
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryTreeResponse
)

# Import service interface for dependency injection
from app.services.category_service import CategoryService
from app.dependencies import get_category_service

# Configure module logger
logger = logging.getLogger(__name__)

# Create router instance for category endpoints
router = APIRouter()

@router.get("/categories", response_model=List[CategoryResponse], summary="Get all categories")
async def get_categories(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    status: Optional[str] = Query(None, description="Filter by status"),
    featured_only: bool = Query(False, description="Show only featured categories"),
    parent_id: Optional[str] = Query(None, description="Filter by parent category"),
    category_service: CategoryService = Depends(get_category_service)
) -> List[CategoryResponse]:
    """
    Retrieve a list of categories with optional filtering and pagination.
    
    Args:
        page (int): Page number for pagination
        per_page (int): Number of items per page
        search (str, optional): Search query for name or description
        status (str, optional): Filter by category status
        featured_only (bool): Show only featured categories
        parent_id (str, optional): Filter by parent category ID
        category_service (CategoryService): Injected category service instance
    
    Returns:
        List[CategoryResponse]: List of categories matching the criteria
    
    Raises:
        HTTPException: If validation fails or service error occurs
    """
    try:
        logger.info(f"Fetching categories - Page: {page}, Per page: {per_page}")
        
        categories = await category_service.get_categories(
            page=page,
            per_page=per_page,
            search=search,
            status=status,
            featured_only=featured_only,
            parent_id=parent_id
        )
        
        logger.info(f"Successfully retrieved {len(categories)} categories")
        return categories
        
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching categories"
        )

@router.get("/categories/tree", response_model=List[CategoryTreeResponse], summary="Get category tree")
async def get_category_tree(
    category_service: CategoryService = Depends(get_category_service)
) -> List[CategoryTreeResponse]:
    """
    Retrieve categories organized in a hierarchical tree structure.
    
    This endpoint returns all categories organized by their parent-child
    relationships, making it easy to display hierarchical navigation.
    
    Args:
        category_service (CategoryService): Injected category service instance
    
    Returns:
        List[CategoryTreeResponse]: Hierarchical tree of categories
    
    Raises:
        HTTPException: If service error occurs
    """
    try:
        logger.info("Fetching category tree structure")
        
        tree = await category_service.get_category_tree()
        
        logger.info(f"Successfully retrieved category tree with {len(tree)} root categories")
        return tree
        
    except Exception as e:
        logger.error(f"Error fetching category tree: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the category tree"
        )

@router.get("/categories/{category_id}", response_model=CategoryResponse, summary="Get category by ID")
async def get_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
) -> CategoryResponse:
    """
    Retrieve a specific category by its ID.
    
    Args:
        category_id (str): The unique identifier of the category
        category_service (CategoryService): Injected category service instance
    
    Returns:
        CategoryResponse: The requested category data
    
    Raises:
        HTTPException: If category not found or service error occurs
    """
    try:
        logger.info(f"Fetching category with ID: {category_id}")
        
        category = await category_service.get_category_by_id(category_id)
        
        if not category:
            logger.warning(f"Category not found: {category_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        logger.info(f"Successfully retrieved category: {category.name}")
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the category"
        )

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Create a new category")
async def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service)
) -> CategoryResponse:
    """
    Create a new category in the library system.
    
    Args:
        category_data (CategoryCreate): The category data to create
        category_service (CategoryService): Injected category service instance
    
    Returns:
        CategoryResponse: The created category data with generated ID
    
    Raises:
        HTTPException: If validation fails or service error occurs
    """
    try:
        logger.info(f"Creating new category: {category_data.name}")
        
        new_category = await category_service.create_category(category_data)
        
        logger.info(f"Successfully created category with ID: {new_category.id}")
        return new_category
        
    except ValueError as e:
        logger.error(f"Validation error in create_category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the category"
        )

@router.put("/categories/{category_id}", response_model=CategoryResponse, summary="Update a category")
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service)
) -> CategoryResponse:
    """
    Update an existing category with new data.
    
    Args:
        category_id (str): The unique identifier of the category to update
        category_data (CategoryUpdate): The updated category data
        category_service (CategoryService): Injected category service instance
    
    Returns:
        CategoryResponse: The updated category data
    
    Raises:
        HTTPException: If category not found or service error occurs
    """
    try:
        logger.info(f"Updating category with ID: {category_id}")
        
        updated_category = await category_service.update_category(category_id, category_data)
        
        if not updated_category:
            logger.warning(f"Category not found for update: {category_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        logger.info(f"Successfully updated category: {updated_category.name}")
        return updated_category
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in update_category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the category"
        )

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a category")
async def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
) -> None:
    """
    Delete a category from the library system.
    
    Note: This operation will fail if the category has associated books or subcategories.
    
    Args:
        category_id (str): The unique identifier of the category to delete
        category_service (CategoryService): Injected category service instance
    
    Returns:
        None: Returns 204 No Content on successful deletion
    
    Raises:
        HTTPException: If category not found, has dependencies, or service error occurs
    """
    try:
        logger.info(f"Deleting category with ID: {category_id}")
        
        success = await category_service.delete_category(category_id)
        
        if not success:
            logger.warning(f"Category not found for deletion: {category_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        
        logger.info(f"Successfully deleted category with ID: {category_id}")
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Cannot delete category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error deleting category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the category"
        )

@router.get("/categories/{category_id}/books", summary="Get books in category")
async def get_category_books(
    category_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    category_service: CategoryService = Depends(get_category_service)
) -> List[dict]:
    """
    Get all books in a specific category.
    
    Args:
        category_id (str): The unique identifier of the category
        page (int): Page number for pagination
        per_page (int): Number of items per page
        category_service (CategoryService): Injected category service instance
    
    Returns:
        List[dict]: Paginated list of books in the category
    
    Raises:
        HTTPException: If category not found or service error occurs
    """
    try:
        logger.info(f"Fetching books for category ID: {category_id}")
        
        books = await category_service.get_category_books(category_id, page, per_page)
        
        logger.info(f"Successfully retrieved {len(books)} books for category: {category_id}")
        return books
        
    except Exception as e:
        logger.error(f"Error fetching category books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching category's books"
        )