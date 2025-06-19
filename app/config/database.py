"""
Database Configuration Module

This module handles MongoDB connection setup and initialization
using Beanie ODM for async document operations.

Responsibilities:
- Establish MongoDB connection using Motor driver
- Initialize Beanie ODM with document models
- Handle database configuration and error management
"""

import os
import logging
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

# Import all document models for Beanie initialization
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category

# Configure module logger
logger = logging.getLogger(__name__)

# Global MongoDB client instance
_mongodb_client: Optional[AsyncIOMotorClient] = None

async def init_db() -> None:
    """
    Initialize database connection and Beanie ODM.
    
    This function establishes a connection to MongoDB using the Motor
    async driver and initializes Beanie ODM with all document models.
    
    Raises:
        Exception: If database connection or initialization fails
    """
    global _mongodb_client
    
    try:
        # Get database configuration from environment variables
        mongodb_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        database_name = os.getenv("MONGO_DB_NAME", "library_db")
        
        logger.info(f"Connecting to MongoDB: {database_name}")
        
        # Create async MongoDB client
        _mongodb_client = AsyncIOMotorClient(mongodb_uri)
        
        # Get database instance
        database = _mongodb_client[database_name]
        
        # Test the connection
        await _mongodb_client.admin.command('ping')
        logger.info("MongoDB connection established successfully")
        
        # Initialize Beanie ODM with document models
        await init_beanie(
            database=database,
            document_models=[Book, Author, Category]
        )
        
        logger.info("Beanie ODM initialized with document models")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

async def close_db() -> None:
    """
    Close database connection.
    
    This function should be called during application shutdown
    to properly close the MongoDB connection.
    """
    global _mongodb_client
    
    if _mongodb_client:
        _mongodb_client.close()
        logger.info("Database connection closed")

def get_database():
    """
    Get the current database instance.
    
    Returns:
        AsyncIOMotorDatabase: The current database instance
        
    Raises:
        RuntimeError: If database is not initialized
    """
    if not _mongodb_client:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    database_name = os.getenv("MONGO_DB_NAME", "library_db")
    return _mongodb_client[database_name]