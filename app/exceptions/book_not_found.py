from app.exceptions.library_exception import LibraryException


class BookNotFoundException(LibraryException):
    """Excepción cuando no se encuentra un libro"""
    
    def __init__(self, message: str = "Libro no encontrado"):
        super().__init__(message, "BOOK_NOT_FOUND")