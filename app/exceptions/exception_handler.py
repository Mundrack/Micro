# Import necessary components from FastAPI and other libraries.
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# Import custom exception classes from the application's modules.
from app.exceptions.library_exception import LibraryException
from app.exceptions.book_not_found import BookNotFoundException

# Get a logger instance for the current module.
logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    """Set up global exception handlers for the FastAPI application."""
    
    # This decorator registers the function below as the handler for LibraryException.
    @app.exception_handler(LibraryException)
    async def library_exception_handler(request: Request, exc: LibraryException):
        # Log the custom library error.
        logger.error(f"LibraryException: {exc.message}")
        # Return a custom JSON response with a 400 Bad Request status.
        return JSONResponse(
            status_code=400,
            content={
                "error": "Library Error",
                "message": exc.message,
                "error_code": exc.error_code
            }
        )
    
    # This decorator registers the function below as the handler for BookNotFoundException.
    @app.exception_handler(BookNotFoundException)
    async def book_not_found_handler(request: Request, exc: BookNotFoundException):
        # Log the specific error when a book is not found.
        logger.error(f"BookNotFoundException: {exc.message}")
        # Return a JSON response with a 404 Not Found status.
        return JSONResponse(
            status_code=404,
            content={
                "error": "Book Not Found",
                "message": exc.message,
                "error_code": exc.error_code
            }
        )
    
    # This decorator handles FastAPI's request validation errors.
    # It's triggered when incoming data doesn't match the Pydantic models.
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Log the detailed validation errors.
        logger.error(f"Validation error: {exc.errors()}")
        # Return a 422 Unprocessable Entity response with details of the validation failure.
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "message": "Datos de entrada inválidos",
                "details": exc.errors()
            }
        )
    
    # This decorator handles standard HTTP exceptions raised by FastAPI/Starlette.
    # For example, `raise HTTPException(status_code=401, detail="Not authenticated")`.
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Log the HTTP exception with its status code and detail message.
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        # Return a JSON response that reflects the exception's status and detail.
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail
            }
        )
    
    # This is a generic, catch-all handler for any exception not caught by the handlers above.
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        # Log the unexpected error, including the full stack trace for debugging purposes.
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        # Return a generic 500 Internal Server Error to avoid leaking implementation details.
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Ha ocurrido un error interno del servidor"
            }
        )