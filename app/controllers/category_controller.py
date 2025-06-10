from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.services.abstract.category_service import CategoryService
from app.services.impl.category_service_impl import CategoryServiceImpl
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.exceptions.library_exception import LibraryException

router = APIRouter()


def get_category_service() -> CategoryService:
    """Inyección de dependencias para el servicio de categorías"""
    return CategoryServiceImpl()


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service)
):
    """Crear una nueva categoría"""
    try:
        category = await category_service.create_category(category_data)
        return CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    """Obtener una categoría por ID"""
    category = await category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        description=category.description,
        created_at=category.created_at,
        updated_at=category.updated_at
    )


@router.get("/categories", response_model=List[CategoryResponse])
async def get_all_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_service: CategoryService = Depends(get_category_service)
):
    """Obtener todas las categorías con paginación"""
    categories = await category_service.get_all_categories(skip=skip, limit=limit)
    
    return [
        CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
        for category in categories
    ]


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service)
):
    """Actualizar una categoría"""
    try:
        category = await category_service.update_category(category_id, category_data)
        return CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
    except LibraryException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    """Eliminar una categoría"""
    try:
        await category_service.delete_category(category_id)
    except LibraryException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/categories/search", response_model=List[CategoryResponse])
async def search_categories(
    name: str = Query(..., min_length=1),
    category_service: CategoryService = Depends(get_category_service)
):
    """Buscar categorías por nombre"""
    categories = await category_service.search_categories_by_name(name)
    
    return [
        CategoryResponse(
            id=str(category.id),
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
        for category in categories
    ]