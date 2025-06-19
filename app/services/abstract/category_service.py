"""
Category Service Interface

This module defines the abstract interface for category-related business operations.
It provides contracts for category management, hierarchical operations,
and relationship handling.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.schemas.category_schema import (
    CategoryCreate, 
    CategoryUpdate, 
    CategoryResponse,
    CategoryTreeResponse
)

class CategoryService(ABC):
    """
    Abstract base class defining the contract for category service operations.
    
    This interface ensures consistent category service implementations
    with support for hierarchical category management.
    """

    @abstractmethod
    async def get_categories(
        self,
        page: int = 1,
        per_page: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None,
        featured_only: bool = False,
        parent_id: Optional[str] = None
    ) -> List[CategoryResponse]:
        """
        Retrieve categories with optional filtering and pagination.
        
        Args:
            page (int): Page number for pagination
            per_page (int): Number of items per page
            search (str, optional): Search query for name or description
            status (str, optional): Filter by status
            featured_only (bool): Show only featured categories
            parent_id (str, optional): Filter by parent category
            
        Returns:
            List[CategoryResponse]: List of categories matching criteria
        """
        pass

    @abstractmethod
    async def get_category_tree(self) -> List[CategoryTreeResponse]:
        """
        Retrieve categories organized in hierarchical tree structure.
        
        Returns:
            List[CategoryTreeResponse]: Hierarchical category tree
        """
        pass

    @abstractmethod
    async def get_category_by_id(self, category_id: str) -> Optional[CategoryResponse]:
        """
        Retrieve a specific category by ID.
        
        Args:
            category_id (str): The unique identifier of the category
            
        Returns:
            Optional[CategoryResponse]: The category data if found, None otherwise
        """
        pass

    @abstractmethod
    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        """
        Create a new category with validation.
        
        Args:
            category_data (CategoryCreate): The category data to create
            
        Returns:
            CategoryResponse: The created category data
            
        Raises:
            ValueError: If validation fails or slug already exists
        """
        pass

    @abstractmethod
    async def update_category(self, category_id: str, category_data: CategoryUpdate) -> Optional[CategoryResponse]:
        """
        Update an existing category.
        
        Args:
            category_id (str): The unique identifier of the category
            category_data (CategoryUpdate): The updated category data
            
        Returns:
            Optional[CategoryResponse]: Updated category data if successful, None if not found
            
        Raises:
            ValueError: If validation fails
        """
        pass

    @abstractmethod
    async def delete_category(self, category_id: str) -> bool:
        """
        Delete a category from the system.
        
        Args:
            category_id (str): The unique identifier of the category
            
        Returns:
            bool: True if deletion successful, False if not found
            
        Raises:
            ValueError: If category has associated books or subcategories
        """
        pass

    @abstractmethod
    async def get_category_books(self, category_id: str, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Get books in a specific category with pagination.
        
        Args:
            category_id (str): The unique identifier of the category
            page (int): Page number for pagination
            per_page (int): Number of items per page
            
        Returns:
            List[Dict[str, Any]]: Paginated list of books in the category
        """
        pass

    @abstractmethod
    async def update_book_count(self, category_id: str) -> None:
        """
        Update the book count for a category.
        
        Args:
            category_id (str): The unique identifier of the category
        """
        pass

    @abstractmethod
    async def get_subcategories(self, parent_id: str) -> List[CategoryResponse]:
        """
        Get all subcategories of a parent category.
        
        Args:
            parent_id (str): The unique identifier of the parent category
            
        Returns:
            List[CategoryResponse]: List of subcategories
        """
        pass