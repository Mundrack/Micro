from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.services.abstract.book_service import BookService
from app.services.impl.book_service_impl import BookServiceImpl
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.exceptions.book_not_found import BookNotFoundException

router = APIRouter()


def get_book_service() -> BookService:
    """Inyección de dependencias para el servicio de libros"""
    return BookServiceImpl()


@router.post("/books", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """Crear un nuevo libro"""
    try:
        book = await book_service.create_book(book_data)
        return BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Obtener un libro por ID"""
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return BookResponse(
        id=str(book.id),
        title=book.title,
        isbn=book.isbn,
        published_date=book.published_date,
        available=book.available,
        author_id=str(book.author_id),
        category_id=str(book.category_id),
        created_at=book.created_at,
        updated_at=book.updated_at
    )


@router.get("/books", response_model=List[BookResponse])
async def get_all_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    book_service: BookService = Depends(get_book_service)
):
    """Obtener todos los libros con paginación"""
    books = await book_service.get_all_books(skip=skip, limit=limit)
    
    return [
        BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        for book in books
    ]


@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    book_service: BookService = Depends(get_book_service)
):
    """Actualizar un libro"""
    try:
        book = await book_service.update_book(book_id, book_data)
        return BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
    except BookNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/books/{book_id}", status_code=204)
async def delete_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Eliminar un libro"""
    try:
        await book_service.delete_book(book_id)
    except BookNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/books/search", response_model=List[BookResponse])
async def search_books(
    title: str = Query(..., min_length=1),
    book_service: BookService = Depends(get_book_service)
):
    """Buscar libros por título"""
    books = await book_service.search_books_by_title(title)
    
    return [
        BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        for book in books
    ]


@router.get("/books/author/{author_id}", response_model=List[BookResponse])
async def get_books_by_author(
    author_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Obtener libros por autor"""
    books = await book_service.get_books_by_author(author_id)
    
    return [
        BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        for book in books
    ]


@router.get("/books/category/{category_id}", response_model=List[BookResponse])
async def get_books_by_category(
    category_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """Obtener libros por categoría"""
    books = await book_service.get_books_by_category(category_id)
    
    return [
        BookResponse(
            id=str(book.id),
            title=book.title,
            isbn=book.isbn,
            published_date=book.published_date,
            available=book.available,
            author_id=str(book.author_id),
            category_id=str(book.category_id),
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        for book in books
    ]