from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.config.database import init_database
from app.config.settings import settings
from app.controllers.book_controller import router as book_router
from app.controllers.author_controller import router as author_router
from app.controllers.category_controller import router as category_router
from app.exceptions.exception_handler import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_database()
    yield
    # Shutdown
    pass


# Crear instancia de FastAPI
app = FastAPI(
    title="Library Microservice",
    description="Microservicio independiente para gestión de librería",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar manejadores de excepciones
setup_exception_handlers(app)

# Registrar rutas
app.include_router(book_router, prefix="/api", tags=["books"])
app.include_router(author_router, prefix="/api", tags=["authors"])
app.include_router(category_router, prefix="/api", tags=["categories"])


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "library-microservice",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Library Microservice API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )