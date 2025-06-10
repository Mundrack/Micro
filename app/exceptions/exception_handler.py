from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from app.exceptions.library_exception import LibraryException
from app.exceptions.book_not_found import BookNotFoundException

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    """Configurar manejadores globales de excepciones"""
    
    @app.exception_handler(LibraryException)
    async def library_exception_handler(request: Request, exc: LibraryException):
        logger.error(f"LibraryException: {exc.message}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "Library Error",
                "message": exc.message,
                "error_code": exc.error_code
            }
        )
    
    @app.exception_handler(BookNotFoundException)
    async def book_not_found_handler(request: Request, exc: BookNotFoundException):
        logger.error(f"BookNotFoundException: {exc.message}")
        return JSONResponse(
            status_code=404,
            content={
                "error": "Book Not Found",
                "message": exc.message,
                "error_code": exc.error_code
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "message": "Datos de entrada inválidos",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Ha ocurrido un error interno del servidor"
            }
        )