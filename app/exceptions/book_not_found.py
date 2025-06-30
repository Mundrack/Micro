# Import the base exception class from which this class will inherit.
from app.exceptions.library_exception import LibraryException


# Define a specific exception for cases where a book cannot be found.
# It inherits from LibraryException, making it part of our custom exception hierarchy.
class BookNotFoundException(LibraryException):
    """Exception raised when a book is not found"""
    
    # The constructor for this specific exception.
    # It takes an optional message, with a default value.
    def __init__(self, message: str = "Libro no encontrado"):
        # Call the constructor of the parent class (LibraryException).
        # We pass the provided message and a hardcoded, specific error code 'BOOK_NOT_FOUND'.
        super().__init__(message, "BOOK_NOT_FOUND")