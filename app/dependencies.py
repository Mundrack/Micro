"""
Dependency Injection Configuration

This module defines the dependency injection setup for the application.
It creates and configures service instances and their dependencies,
following the Dependency Inversion Principle for better testability
and maintainability.

The dependencies are cached using @lru_cache to ensure singleton
behavior and improve performance.
"""

from functools import lru_cache
import logging

# Import service interfaces
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.services.category_service import CategoryService

# Import service implementations
from app.services.impl.book_service_impl import BookServiceImpl
from app.services.impl.author_service_impl import AuthorServiceImpl
from app.services.impl.category_service_impl import CategoryServiceImpl

# Import repository implementations
from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.category_repository import CategoryRepository

# Configure module logger
logger = logging.getLogger(__name__)

# ============================================================================
# Repository Dependencies
# ============================================================================

@lru_cache()
def get_book_repository() -> BookRepository:
    """
    Create and return a BookRepository instance.
    
    This function creates a singleton# Library Microservice - Complete Codebase
    instance of BookRepository using the LRU cache decorator.
    """
    logger.debug("Creating BookRepository instance")
    return BookRepository()