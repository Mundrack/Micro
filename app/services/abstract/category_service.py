from abc import ABC, abstractmethod
from typing import List, Optional

from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


class CategoryService(ABC):
    """Interfaz abstracta para el servicio de categorías"""
    
    @abstractmethod
    async def create_category(self, category_data: CategoryCreate) -> Category:
        """Crear una nueva categoría"""
        pass
    
    @abstractmethod
    async def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """Obtener una categoría por su ID"""
        pass
    
    @abstractmethod
    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtener todas las categorías con paginación"""
        pass
    
    @abstractmethod
    async def update_category(self, category_id: str, category_data: CategoryUpdate) -> Optional[Category]:
        """Actualizar una categoría existente"""
        pass
    
    @abstractmethod
    async def delete_category(self, category_id: str) -> bool:
        """Eliminar una categoría"""
        pass
    
    @abstractmethod
    async def search_categories_by_name(self, name: str) -> List[Category]:
        """Buscar categorías por nombre"""
        pass