from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import re

from app.services.abstract.category_service import CategoryService
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.exceptions.library_exception import LibraryException


class CategoryServiceImpl(CategoryService):
    """Implementación concreta del servicio de categorías"""
    
    async def create_category(self, category_data: CategoryCreate) -> Category:
        """Crear una nueva categoría"""
        category = Category(
            name=category_data.name,
            description=category_data.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await category.insert()
        return category
    
    async def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """Obtener una categoría por su ID"""
        try:
            category = await Category.get(ObjectId(category_id))
            return category
        except Exception:
            return None
    
    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Obtener todas las categorías con paginación"""
        categories = await Category.find_all().skip(skip).limit(limit).to_list()
        return categories
    
    async def update_category(self, category_id: str, category_data: CategoryUpdate) -> Optional[Category]:
        """Actualizar una categoría existente"""
        category = await self.get_category_by_id(category_id)
        if not category:
            raise LibraryException(f"Categoría con ID {category_id} no encontrada")
        
        # Actualizar solo los campos proporcionados
        update_data = category_data.model_dump(exclude_unset=True)
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            
            # Actualizar el documento
            for field, value in update_data.items():
                setattr(category, field, value)
            
            await category.save()
        
        return category
    
    async def delete_category(self, category_id: str) -> bool:
        """Eliminar una categoría"""
        category = await self.get_category_by_id(category_id)
        if not category:
            raise LibraryException(f"Categoría con ID {category_id} no encontrada")
        
        await category.delete()
        return True
    
    async def search_categories_by_name(self, name: str) -> List[Category]:
        """Buscar categorías por nombre (búsqueda case-insensitive)"""
        regex_pattern = re.compile(name, re.IGNORECASE)
        categories = await Category.find({"name": {"$regex": regex_pattern}}).to_list()
        return categories