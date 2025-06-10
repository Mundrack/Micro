from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.author import Author
from app.schemas.author_schema import AuthorCreate, AuthorUpdate


class AuthorService(ABC):
    """Interfaz abstracta para el servicio de autores"""
    
    @abstractmethod
    async def create_author(self, author_data: AuthorCreate) -> Author:
        """Crear un nuevo autor"""
        pass
    
    @abstractmethod
    async def get_author_by_id(self, author_id: str) -> Optional[Author]:
        """Obtener un autor por su ID"""
        pass
    
    @abstractmethod
    async def get_all_authors(self, skip: int = 0, limit: int = 100) -> List[Author]:
        """Obtener todos los autores con paginación"""
        pass
    
    @abstractmethod
    async def update_author(self, author_id: str, author_data: AuthorUpdate) -> Optional[Author]:
        """Actualizar un autor existente"""
        pass
    
    @abstractmethod
    async def delete_author(self, author_id: str) -> bool:
        """Eliminar un autor"""
        pass
    
    @abstractmethod
    async def search_authors_by_name(self, name: str) -> List[Author]:
        """Buscar autores por nombre"""
        pass