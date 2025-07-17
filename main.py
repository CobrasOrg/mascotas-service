import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Cargar variables de entorno desde .env
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.db.database import db
from app.api.v1.endpoints.pets import router as pets_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=None,  # Se reemplazará abajo
    openapi_tags=[
        {
            "name": "Mascotas",
            "description": "Operaciones para gestionar mascotas de usuarios"
        }
    ]
)

# Configuración de seguridad para Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        routes=app.routes,
    )
    
    # Agregar configuración de seguridad
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa tu token JWT. Para desarrollo puedes usar: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
        }
    }
    
    # Aplicar seguridad a todos los endpoints protegidos
    for path in openapi_schema["paths"]:
        if path.startswith("/api/v1/pets") and path != "/api/v1/pets/photo/{pet_id}":
            for method in openapi_schema["paths"][path]:
                if method.lower() in ["get", "post", "put", "delete"]:
                    openapi_schema["paths"][path][method]["security"] = [
                        {"BearerAuth": []}
                    ]
    
    # Configurar seguridad global para que se aplique automáticamente
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Lifespan para inicialización y cierre
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect_to_mongo()
    yield
    await db.close_mongo_connection()

app.router.lifespan_context = lifespan

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pets_router, prefix=f"{settings.API_V1_STR}/pets", tags=["Mascotas"])
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Mascotas Service API",
        "version": settings.VERSION,
        "features": [
            "Gestión de mascotas",
            "Soporte para imágenes con Cloudinary",
            "Base de datos MongoDB",
            "Autenticación JWT",
            "Endpoints para propietarios de mascotas"
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "authentication": {
            "type": "JWT Bearer Token",
            "example_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
        }
    }

@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la aplicación
    """
    try:
        # Verificar MongoDB
        await db.client.admin.command('ping')
        mongo_status = "healthy"
    except Exception:
        mongo_status = "unhealthy"
    
    return {
        "status": "ok",
        "mongodb": mongo_status,
        "cloudinary": "configured"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True) 