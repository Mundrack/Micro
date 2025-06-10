from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import re

from app.services.abstract.book_service import BookService
from app.models.book import Book
from app.schemas.book_schema import BookCreate, BookUpdate
from app.exceptions.book_not_found import BookNotFoundException


class BookServiceImpl(BookService):
    """Implementación concreta del servicio de libros"""
    
    async def create_book(self, book_data: BookCreate) -> Book:
        """Crear un nuevo libro"""
        book = Book(
            title=book_data.title,
            isbn=book_data.isbn,
            published_date=book_data.published_date,
            available=book_data.available,
            author_id=ObjectId(book_data.author_id),
            category_id=ObjectId(book_data.category_id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await book.insert()
        return book
    
    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Obtener un libro por su ID"""
        try:
            book = await Book.get(ObjectId(book_id))
            return book
        except Exception:
            return None
    
    async def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """Obtener todos los libros con paginación"""
        books = await Book.find_all().skip(skip).limit(limit).to_list()
        return books
    
    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[Book]:
        """Actualizar un libro existente"""
        book = await self.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundException(f"Libro con ID {book_id} no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = book_data.model_dump(exclude_unset=True)
        
        if update_data:
            # Convertir string IDs a ObjectId si están presentes
            if "author_id" in update_data:
                update_data["author_id"] = ObjectId(update_data["author_id"])
            if "category_id" in update_data:
                update_data["category_id"] = ObjectId(update_data["category_id"])
            
            update_data["updated_at"] = datetime.utcnow()
            
            # Actualizar el documento
            for field, value in update_data.items():
                setattr(book, field, value)
            
            await book.save()
        
        return book
    
    async def delete_book(self, book_id: str) -> bool:
        """Eliminar un libro"""
        book = await self.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundException(f"Libro con ID {book_id} no encontrado")
        
        await book.delete()
        return True
    
    async def search_books_by_title(self, title: str) -> List[Book]:
        """Buscar libros por título (búsqueda case-insensitive)"""
        # Crear regex para búsqueda case-insensitive
        regex_pattern = re.compile(title, re.IGNORECASE)
        books = await Book.find({"title": {"$regex": regex_pattern}}).to_list()
        return books
    
    async def get_books_by_author(self, author_id: str) -> List[Book]:
        """Obtener libros por autor"""
        books = await Book.find({"author_id": ObjectId(author_id)}).to_list()
        return books
    
    async def get_books_by_category(self, category_id: str) -> List[Book]:
        """Obtener libros por categoría"""
        books = await Book.find({"category_id": ObjectId(category_id)}).to_list()
        return books