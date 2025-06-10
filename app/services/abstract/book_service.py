from abc import ABC, abstractmethod
from typing import List, Optional
from bson import ObjectId

from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookUpdate


class BookService(ABC):
    """Interfaz abstracta para el servicio de libros"""
    
    @abstractmethod
    async def create_book(self, book_data: BookCreate) -> Book:
        """Crear un nuevo libro"""
        pass
    
    @abstractmethod
    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Obtener un libro por su ID"""
        pass
    
    @abstractmethod
    async def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Obtener todos los libros con paginación"""
        pass
    
    @abstractmethod
    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[Book]:
        """Actualizar un libro existente"""
        pass
    
    @abstractmethod
    async def delete_book(self, book_id: str) -> bool:
        """Eliminar un libro"""
        pass
    
    @abstractmethod
    async def search_books_by_title(self, title: str) -> List[Book]:
        """Buscar libros por título"""
        pass
    
    @abstractmethod
    async def get_books_by_author(self, author_id: str) -> List[Book]:
        """Obtener libros por autor"""
        pass
    
    @abstractmethod
    async def get_books_by_category(self, category_id: str) -> List[Book]:
        """Obtener libros por categoría"""
        pass