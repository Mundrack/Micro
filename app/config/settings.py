import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB Atlas
    mongo_uri: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/library_db')
    mongo_db_name: str = os.getenv('MONGO_DB_NAME', 'library_db')
    
    # Application
    app_host: str = os.getenv('APP_HOST', '0.0.0.0')
    app_port: int = int(os.getenv('APP_PORT', '8000'))
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Logging
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_path: str = os.getenv('LOG_PATH', '/var/log/library')
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', 'development-key-change-in-production')
    
    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()