import os
from pydantic import BaseSettings


class Config(BaseSettings):
    """Configuración alternativa del microservicio"""
    
    # MongoDB Atlas
    mongo_uri: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/library_db')
    mongo_db_name: str = os.getenv('MONGO_DB_NAME', 'library_db')
    
    # Application
    app_host: str = os.getenv('APP_HOST', '0.0.0.0')
    app_port: int = int(os.getenv('APP_PORT', '8000'))
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'development-key')
    
    # Logging
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    def get_mongodb_uri(self) -> str:
        """Obtener URI de MongoDB"""
        return self.mongo_uri
    
    def is_development(self) -> bool:
        """Verificar si está en modo desarrollo"""
        return self.debug
    
    def get_app_config(self) -> dict:
        """Obtener configuración de la aplicación"""
        return {
            "host": self.app_host,
            "port": self.app_port,
            "debug": self.debug,
            "log_level": self.log_level
        }


# Instancia global de configuración
config = Config()