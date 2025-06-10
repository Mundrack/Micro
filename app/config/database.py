from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import logging

from app.config.settings import settings
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category

logger = logging.getLogger(__name__)


async def init_database():
    """Inicializar conexión a MongoDB Atlas y configurar Beanie"""
    try:
        # Crear cliente de MongoDB
        client = AsyncIOMotorClient(settings.mongo_uri)
        
        # Obtener la base de datos
        database = client[settings.mongo_db_name]
        
        # Inicializar Beanie con los modelos
        await init_beanie(
            database=database,
            document_models=[Book, Author, Category]
        )
        
        logger.info(f"Conectado exitosamente a MongoDB Atlas: {settings.mongo_db_name}")
        
        # Verificar conexión
        await client.admin.command('ping')
        logger.info("Ping a MongoDB Atlas exitoso")
        
    except Exception as e:
        logger.error(f"Error conectando a MongoDB Atlas: {e}")
        raise e


async def get_database():
    """Obtener instancia de la base de datos"""
    client = AsyncIOMotorClient(settings.mongo_uri)
    return client[settings.mongo_db_name]