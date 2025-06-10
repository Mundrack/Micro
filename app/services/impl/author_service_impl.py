from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import re

from app.services.abstract.author_service import AuthorService
from app.models.author import Author
from app.schemas.author_schema import AuthorCreate, AuthorUpdate
from app.exceptions.library_exception import LibraryException


class AuthorServiceImpl(AuthorService):
    """Implementación concreta del servicio de autores"""
    
    async def create_author(self, author_data: AuthorCreate) -> Author:
        """Crear un nuevo autor"""
        author = Author(
            name=author_data.name,
            biography=author_data.biography,
            birth_date=author_data.birth_date,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await author.insert()
        return author
    
    async def get_author_by_id(self, author_id: str) -> Optional[Author]:
        """Obtener un autor por su ID"""
        try:
            author = await Author.get(ObjectId(author_id))
            return author
        except Exception:
            return None
    
    async def get_all_authors(self, skip: int = 0, limit: int = 100) -> List[Author]:
        """Obtener todos los autores con paginación"""
        authors = await Author.find_all().skip(skip).limit(limit).to_list()
        return authors
    
    async def update_author(self, author_id: str, author_data: AuthorUpdate) -> Optional[Author]:
        """Actualizar un autor existente"""
        author = await self.get_author_by_id(author_id)
        if not author:
            raise LibraryException(f"Autor con ID {author_id} no encontrado")
        
        # Actualizar solo los campos proporcionados
        update_data = author_data.model_dump(exclude_unset=True)
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            # Actualizar el documento
            for field, value in update_data.items():
                setattr(author, field, value)
            
            await author.save()
        
        return author
    
    async def delete_author(self, author_id: str) -> bool:
        """Eliminar un autor"""
        author = await self.get_author_by_id(author_id)
        if not author:
            raise LibraryException(f"Autor con ID {author_id} no encontrado")
        
        await author.delete()
        return True
    
    async def search_authors_by_name(self, name: str) -> List[Author]:
        """Buscar autores por nombre (búsqueda case-insensitive)"""
        regex_pattern = re.compile(name, re.IGNORECASE)
        authors = await Author.find({"name": {"$regex": regex_pattern}}).to_list()
        return authors