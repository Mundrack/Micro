# A base exception class for the library microservice.
# It inherits from Python's built-in Exception class.
class LibraryException(Exception):
    """Base exception for the library microservice"""
    
    # The constructor for our custom exception.
    def __init__(self, message: str, error_code: str = None):
        # The human-readable message for the error.
        self.message = message
        # An optional, specific code to identify the error.
        self.error_code = error_code
        # Call the constructor of the parent class (Exception).
        # This ensures the exception behaves like a standard Python exception.
        super().__init__(self.message)