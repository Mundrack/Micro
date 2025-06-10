from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.services.abstract.author_service import AuthorService
from app.services.impl.author_service_impl import AuthorServiceImpl
from app.schemas.author_schema import AuthorCreate, AuthorUpdate, AuthorResponse
from app.exceptions.library_exception import LibraryException

router = APIRouter()


def get_author_service() -> AuthorService:
    """Inyección de dependencias para el servicio de autores"""
    return AuthorServiceImpl()


@router.post("/authors", response_model=AuthorResponse, status_code=201)
async def create_author(
    author_data: AuthorCreate,
    author_service: AuthorService = Depends(get_author_service)
):
    """Crear un nuevo autor"""
    try:
        author = await author_service.create_author(author_data)
        return AuthorResponse(
            id=str(author.id),
            name=author.name,
            biography=author.biography,
            birth_date=author.birth_date,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/authors/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: str,
    author_service: AuthorService = Depends(get_author_service)
):
    """Obtener un autor por ID"""
    author = await author_service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
    return AuthorResponse(
        id=str(author.id),
        name=author.name,
        biography=author.biography,
        birth_date=author.birth_date,
        created_at=author.created_at,
        updated_at=author.updated_at
    )


@router.get("/authors", response_model=List[AuthorResponse])
async def get_all_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    author_service: AuthorService = Depends(get_author_service)
):
    """Obtener todos los autores con paginación"""
    authors = await author_service.get_all_authors(skip=skip, limit=limit)
    
    return [
        AuthorResponse(
            id=str(author.id),
            name=author.name,
            biography=author.biography,
            birth_date=author.birth_date,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
        for author in authors
    ]


@router.put("/authors/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: str,
    author_data: AuthorUpdate,
    author_service: AuthorService = Depends(get_author_service)
):
    """Actualizar un autor"""
    try:
        author = await author_service.update_author(author_id, author_data)
        return AuthorResponse(
            id=str(author.id),
            name=author.name,
            biography=author.biography,
            birth_date=author.birth_date,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
    except LibraryException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/authors/{author_id}", status_code=204)
async def delete_author(
    author_id: str,
    author_service: AuthorService = Depends(get_author_service)
):
    """Eliminar un autor"""
    try:
        await author_service.delete_author(author_id)
    except LibraryException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/authors/search", response_model=List[AuthorResponse])
async def search_authors(
    name: str = Query(..., min_length=1),
    author_service: AuthorService = Depends(get_author_service)
):
    """Buscar autores por nombre"""
    authors = await author_service.search_authors_by_name(name)
    
    return [
        AuthorResponse(
            id=str(author.id),
            name=author.name,
            biography=author.biography,
            birth_date=author.birth_date,
            created_at=author.created_at,
            updated_at=author.updated_at
        )
        for author in authors
    ]