class LibraryException(Exception):
    """Excepción base para el microservicio de librería"""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)