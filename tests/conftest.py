import pytest
import pytest_asyncio
import asyncio
import httpx
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

# Importaciones de la aplicación (solo las que no dependen de la app o db)
try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
    
    # Cargar configuración de testing primero
    from tests.test_config import *
    
    # Importaciones que no dependen de la app o db
    from app.core.enums import SpeciesEnum, BloodTypeEnum, BREEDS
    from app.services.cloudinary_service import delete_image
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("💡 Asegúrate de estar en el directorio raíz del proyecto")
    raise

# Tokens de prueba para autenticación
TEST_TOKEN_OWNER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
TEST_TOKEN_CLINIC = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.clinic"

async def get_real_auth_token(user_type: str = "owner") -> str:
    """
    Obtiene un token real de la API de autenticación
    
    Args:
        user_type: Tipo de usuario ('owner' o 'clinic')
        
    Returns:
        str: Token de autenticación
    """
    try:
        # Credenciales de prueba
        credentials = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        # Si es clinic, usar credenciales diferentes
        if user_type == "clinic":
            credentials = {
                "email": "clinic@example.com", 
                "password": "clinic123"
            }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://auth-service-g7nh.onrender.com/api/v1/auth/login",
                json=credentials,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("token", TEST_TOKEN_OWNER if user_type == "owner" else TEST_TOKEN_CLINIC)
            else:
                print(f"⚠️ Error obteniendo token real: {response.status_code}")
                return TEST_TOKEN_OWNER if user_type == "owner" else TEST_TOKEN_CLINIC
                
    except Exception as e:
        print(f"⚠️ Error conectando a auth service: {e}")
        return TEST_TOKEN_OWNER if user_type == "owner" else TEST_TOKEN_CLINIC

def get_auth_headers(user_type: str = "owner") -> dict:
    """
    Genera headers de autenticación para tests
    
    Args:
        user_type: Tipo de usuario ('owner' o 'clinic')
        
    Returns:
        dict: Headers de autenticación
    """
    token = TEST_TOKEN_OWNER if user_type == "owner" else TEST_TOKEN_CLINIC
    return {
        "Authorization": f"Bearer {token}",
        "X-User-Type": user_type
    }

async def get_auth_headers_with_real_token(user_type: str = "owner") -> dict:
    """
    Genera headers de autenticación con token real
    
    Args:
        user_type: Tipo de usuario ('owner' o 'clinic')
        
    Returns:
        dict: Headers de autenticación
    """
    token = await get_real_auth_token(user_type)
    return {
        "Authorization": f"Bearer {token}",
        "X-User-Type": user_type
    }

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def clean_db():
    print("⚠️ Limpieza de base de datos simulada (no async)")
    yield

@pytest.fixture(scope="function")
def client(clean_db):
    import importlib
    import sys
    if "main" in sys.modules:
        importlib.reload(sys.modules["main"])
    from main import app
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client

@pytest_asyncio.fixture
async def sample_pet(clean_db):
    """Create a sample pet for testing"""
    try:
        # Importar aquí para usar la conexión configurada por clean_db
        from app.db.database import db
        from app.models.pet_mongo import PetMongoModel
        
        # Datos de ejemplo (sin campo 'id')
        pet_data = {
            "petName": "Mascota Test",
            "species": SpeciesEnum.canine,
            "breed": "Labrador Retriever",
            "age": 3,
            "weight": 25.5,
            "bloodType": BloodTypeEnum.DEA_1_1_pos,
            "lastVaccination": "2024-01-01",
            "healthStatus": "Sano y vacunado",
            "petPhoto": "https://test.com/foto.jpg",
            "ownerId": "test-owner-123",
            "registeredAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
        
        # Crear la mascota usando el modelo
        pet = await PetMongoModel.create_pet(pet_data)
        print(f"✅ Mascota de prueba creada: {pet.id}")
        yield pet
        
    except Exception as e:
        print(f"❌ Error creando mascota de prueba: {str(e)}")
        yield None

# Funciones útiles adicionales para testing
def get_real_image_bytes() -> bytes:
    """Obtiene bytes de una imagen real para testing"""
    image_path = os.path.join("app", "data", "images", "perro.jpg")
    try:
        with open(image_path, "rb") as img_file:
            return img_file.read()
    except FileNotFoundError:
        # Fallback a imagen sintética si no existe el archivo
        print("⚠️ Imagen real no encontrada, usando imagen sintética")
        image_data = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08'
            b'\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e'
            b'\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342'
            b'\xff\xc0\x00\x11\x08\x00\n\x00\n\x01\x01\x11\x00\x02\x11\x01\x03'
            b'\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        )
        return image_data

def get_image_bytes_for_species(species: str) -> tuple[bytes, str]:
    """Obtiene bytes de imagen y nombre de archivo según la especie"""
    if species.lower() == "feline" or species == SpeciesEnum.feline:
        image_path = os.path.join("app", "data", "images", "gato.jpeg")
        filename = "gato.jpeg"
    else:
        image_path = os.path.join("app", "data", "images", "perro.jpeg")
        filename = "perro.jpeg"
    
    try:
        with open(image_path, "rb") as img_file:
            return img_file.read(), filename
    except FileNotFoundError:
        # Fallback a imagen sintética si no existe el archivo
        print(f"⚠️ Imagen real no encontrada para {species}, usando imagen sintética")
        image_data = get_real_image_bytes()
        return image_data, filename

def create_test_pet_data(species: SpeciesEnum = SpeciesEnum.canine) -> dict:
    """Crea datos de prueba para una mascota"""
    return {
        "petName": "Mascota Test",
        "species": species,
        "breed": "Labrador Retriever" if species == SpeciesEnum.canine else "Siamés",
        "age": 3,
        "weight": 25.5,
        "bloodType": BloodTypeEnum.DEA_1_1_pos,
        "lastVaccination": "2024-01-01",
        "healthStatus": "Sano y vacunado"
    }

# Constantes para testing
TEST_PET_DATA = {
    "petName": "Mascota Test",
    "species": SpeciesEnum.canine,
    "breed": "Labrador Retriever",
    "age": 3,
    "weight": 25.5,
    "bloodType": BloodTypeEnum.DEA_1_1_pos,
    "lastVaccination": "2024-01-01",
    "healthStatus": "Sano y vacunado"
}

TEST_PET_DATA_INVALID = {
    "petName": "",  # Nombre vacío
    "species": "INVALID_SPECIES",  # Especie inválida
    "breed": "Raza Invalida",
    "age": -1,  # Edad negativa
    "weight": -5.0,  # Peso negativo
    "bloodType": "INVALID_BLOOD_TYPE",  # Tipo de sangre inválido
    "lastVaccination": "2024-01-01",
    "healthStatus": "Estado de salud"
} 