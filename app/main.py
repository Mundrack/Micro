"""
Library Microservice - Main Application Entry Point

This module sets up the FastAPI application, configures middleware,
registers routes, and handles application lifecycle events.

Author: Mateo Gabriel Puga Montesdeoca.
Version: 1.0.0
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Import controllers for route registration
from app.controllers import book_controller, author_controller, category_controller
from app.config.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="Library Management Microservice",
    description="A comprehensive RESTful API for library management operations",
    version="1.0.0",
    docs_url="/docs",          # Swagger UI endpoint
    redoc_url="/redoc",        # ReDoc endpoint
    openapi_url="/openapi.json"  # OpenAPI schema endpoint
)

# Configure CORS middleware to allow cross-origin requests
# This is essential for frontend applications running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production, specify exact origins
    allow_credentials=True,      # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)

# Register API route handlers with appropriate prefixes and tags
app.include_router(
    book_controller.router, 
    prefix="/api", 
    tags=["Books"]
)
app.include_router(
    author_controller.router, 
    prefix="/api", 
    tags=["Authors"]
)
app.include_router(
    category_controller.router, 
    prefix="/api", 
    tags=["Categories"]
)

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    This function is executed when the application starts up.
    It initializes the database connection and performs any
    necessary startup operations.
    """
    logger.info("Starting Library Microservice...")
    await init_db()
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    
    This function is executed when the application shuts down.
    It performs cleanup operations like closing database connections.
    """
    logger.info("Shutting down Library Microservice...")

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Application status and version information
    """
    return {
        "status": "healthy",
        "service": "Library Management Microservice",
        "version": "1.0.0"
    }

# Application entry point
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",      # Listen on all available interfaces
        port=8000,           # Default port
        reload=True,         # Auto-reload on code changes (development only)
        log_level="info"     # Logging level
    )