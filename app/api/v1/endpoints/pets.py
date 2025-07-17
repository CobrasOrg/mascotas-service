from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends, Header
from fastapi.responses import StreamingResponse
from typing import List, Optional
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.models.pet_mongo import PetMongoModel
from app.db.database import get_database
from app.services.cloudinary_service import upload_image, delete_image
from app.api.dependencies import get_current_user_id, get_current_user
from motor.motor_asyncio import AsyncIOMotorDatabase
import secrets

router = APIRouter()

@router.get(
    "/",
    response_model=List[PetResponse],
    summary="Obtener todas las mascotas del usuario autenticado",
    description="Retorna todas las mascotas del usuario autenticado basándose en el token JWT.",
    tags=["Mascotas"],
    responses={
        200: {
            "description": "Lista de mascotas del usuario autenticado",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "507f1f77bcf86cd799439011",
                            "petName": "Luna",
                            "species": "Gato",
                            "breed": "Siamés",
                            "age": 3,
                            "weight": 4.5,
                            "bloodType": "A",
                            "lastVaccination": "2024-01-15",
                            "healthStatus": "Saludable",
                            "petPhoto": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/luna.jpg",
                            "ownerId": "user-123"
                        },
                        {
                            "id": "507f1f77bcf86cd799439012",
                            "petName": "Max",
                            "species": "Perro",
                            "breed": "Golden Retriever",
                            "age": 5,
                            "weight": 25.0,
                            "bloodType": "DEA 1.1+",
                            "lastVaccination": "2024-02-20",
                            "healthStatus": "Saludable",
                            "petPhoto": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/max.jpg",
                            "ownerId": "user-123"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Token de autorización requerido o inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token de autorización requerido"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al obtener las mascotas"}
                }
            }
        }
    }
)
async def list_pets(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene todas las mascotas del usuario autenticado.
    
    Args:
        db (AsyncIOMotorDatabase): Instancia de la base de datos
        current_user_id (str): ID del usuario autenticado (obtenido del token JWT)
    
    Returns:
        List[PetResponse]: Lista de mascotas del usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o ocurre un error al obtener las mascotas
    """
    try:
        pets = await PetMongoModel.get_pets_by_owner(current_user_id, db)
        return pets
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al obtener las mascotas"
        )

@router.get(
    "/user/{user_id}",
    response_model=List[PetResponse],
    summary="Obtener mascotas por ID de usuario específico",
    description="Retorna todas las mascotas de un usuario específico. Útil para administradores o consultas específicas.",
    tags=["Mascotas"],
    responses={
        200: {
            "description": "Lista de mascotas del usuario especificado",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "507f1f77bcf86cd799439011",
                            "petName": "Luna",
                            "species": "Gato",
                            "breed": "Siamés",
                            "age": 3,
                            "weight": 4.5,
                            "bloodType": "A",
                            "lastVaccination": "2024-01-15",
                            "healthStatus": "Saludable",
                            "petPhoto": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/luna.jpg",
                            "ownerId": "user-123"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Token de autorización requerido o inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token de autorización requerido"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al obtener las mascotas"}
                }
            }
        }
    }
)
async def get_pets_by_user_id(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Obtiene todas las mascotas de un usuario específico.
    
    Args:
        user_id (str): ID del usuario cuyas mascotas se quieren obtener
        db (AsyncIOMotorDatabase): Instancia de la base de datos
        current_user_id (str): ID del usuario autenticado (obtenido del token JWT)
    
    Returns:
        List[PetResponse]: Lista de mascotas del usuario especificado
        
    Raises:
        HTTPException: Si el token es inválido o ocurre un error al obtener las mascotas
    """
    try:
        pets = await PetMongoModel.get_pets_by_owner(user_id, db)
        return pets
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al obtener las mascotas"
        )

@router.post(
    "/",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva mascota",
    description="Crea una nueva mascota asociada al usuario autenticado. Puede incluir una foto de la mascota (opcional).",
    tags=["Mascotas"],
    responses={
        201: {
            "description": "Mascota creada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": "507f1f77bcf86cd799439013",
                        "petName": "Bella",
                        "species": "Perro",
                        "breed": "Labrador",
                        "age": 2,
                        "weight": 22.5,
                        "bloodType": "DEA 1.1+",
                        "lastVaccination": "2024-03-10",
                        "healthStatus": "Saludable",
                        "petPhoto": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/bella.jpg",
                        "ownerId": "user-123"
                    }
                }
            }
        },
        400: {
            "description": "Error al subir la imagen",
            "content": {
                "application/json": {
                    "example": {"detail": "Error al subir la imagen: Formato de archivo no soportado"}
                }
            }
        },
        401: {
            "description": "Token de autorización requerido o inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token de autorización requerido"}
                }
            }
        },
        422: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "example": {"detail": "La edad debe ser un número positivo"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al crear la mascota"}
                }
            }
        }
    }
)
async def create_pet_endpoint(
    petName: str = Form("Luna", description="Nombre de la mascota", examples=["Luna"]),
    species: str = Form("canine", description="Especie de la mascota (canine, feline)", examples=["canine"]),
    breed: str = Form("Golden Retriever", description="Raza de la mascota", examples=["Golden Retriever"]),
    age: int = Form(3, description="Edad de la mascota en años", examples=[3]),
    weight: float = Form(15.5, description="Peso de la mascota en kilogramos", examples=[15.5]),
    bloodType: str = Form("DEA 1.1+", description="Tipo de sangre de la mascota", examples=["DEA 1.1+"]),
    lastVaccination: str = Form("2024-12-01", description="Fecha de la última vacunación (YYYY-MM-DD)", examples=["2024-12-01"]),
    healthStatus: str = Form("Sano y vacunado", description="Estado de salud de la mascota", examples=["Sano y vacunado"]),
    petPhoto: Optional[UploadFile] = File(None, description="Foto de la mascota (opcional)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Crea una nueva mascota asociada al usuario autenticado.
    Puede incluir una foto de la mascota (opcional).
    
    Args:
        petName (str): Nombre de la mascota
        species (str): Especie de la mascota
        breed (str): Raza de la mascota
        age (int): Edad de la mascota en años
        weight (float): Peso de la mascota en kilogramos
        bloodType (str): Tipo de sangre de la mascota
        lastVaccination (str): Fecha de la última vacunación
        healthStatus (str): Estado de salud de la mascota
        petPhoto (UploadFile): Foto de la mascota (opcional)
        db (AsyncIOMotorDatabase): Instancia de la base de datos
        current_user_id (str): ID del usuario autenticado (obtenido del token JWT)
    
    Returns:
        PetResponse: Mascota creada
        
    Raises:
        HTTPException: Si ocurre un error al crear la mascota o subir la imagen
    """
    try:
        pet_data = PetCreate(
            petName=petName,
            species=species,
            breed=breed,
            age=age,
            weight=weight,
            bloodType=bloodType,
            lastVaccination=lastVaccination,
            healthStatus=healthStatus
        )
        
        # Subir imagen a Cloudinary si se proporciona
        photo_url = None
        if petPhoto:
            try:
                # Generar un ID único para la imagen
                photo_id = secrets.token_hex(12)
                photo_url = upload_image(petPhoto.file, public_id=photo_id)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al subir la imagen: {str(e)}"
                )
        
        # Crear la mascota asociada al usuario autenticado
        pet = await PetMongoModel.create_pet(pet_data, current_user_id, db, photo_url)
        return pet
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al crear la mascota: {str(e)}"
        )

@router.put(
    "/{pet_id}",
    response_model=PetResponse,
    summary="Actualizar mascota existente",
    description="Actualiza la información de una mascota existente. Solo permite actualizar mascotas propias del usuario autenticado.",
    tags=["Mascotas"],
    responses={
        200: {
            "description": "Mascota actualizada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": "507f1f77bcf86cd799439011",
                        "petName": "Luna",
                        "species": "Gato",
                        "breed": "Siamés",
                        "age": 4,
                        "weight": 4.8,
                        "bloodType": "A",
                        "lastVaccination": "2024-04-15",
                        "healthStatus": "Saludable",
                        "petPhoto": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/luna_updated.jpg",
                        "ownerId": "user-123"
                    }
                }
            }
        },
        400: {
            "description": "Error al subir la imagen",
            "content": {
                "application/json": {
                    "example": {"detail": "Error al subir la imagen: Formato de archivo no soportado"}
                }
            }
        },
        401: {
            "description": "Token de autorización requerido o inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token de autorización requerido"}
                }
            }
        },
        403: {
            "description": "No autorizado para modificar esta mascota",
            "content": {
                "application/json": {
                    "example": {"detail": "No tienes permisos para modificar esta mascota"}
                }
            }
        },
        404: {
            "description": "Mascota no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Mascota no encontrada"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al actualizar la mascota"}
                }
            }
        }
    }
)
async def update_pet_endpoint(
    pet_id: str,
    petName: Optional[str] = Form(None, description="Nombre de la mascota"),
    species: Optional[str] = Form(None, description="Especie de la mascota"),
    breed: Optional[str] = Form(None, description="Raza de la mascota"),
    age: Optional[int] = Form(None, description="Edad de la mascota en años"),
    weight: Optional[float] = Form(None, description="Peso de la mascota en kilogramos"),
    bloodType: Optional[str] = Form(None, description="Tipo de sangre de la mascota"),
    lastVaccination: Optional[str] = Form(None, description="Fecha de la última vacunación"),
    healthStatus: Optional[str] = Form(None, description="Estado de salud de la mascota"),
    petPhoto: Optional[UploadFile] = File(None, description="Nueva foto de la mascota (opcional)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Actualiza la información de una mascota existente.
    Solo permite actualizar mascotas propias del usuario autenticado.
    Puede incluir una nueva foto de la mascota (opcional).
    
    Args:
        pet_id (str): ID de la mascota a actualizar
        petName (Optional[str]): Nuevo nombre de la mascota
        species (Optional[str]): Nueva especie de la mascota
        breed (Optional[str]): Nueva raza de la mascota
        age (Optional[int]): Nueva edad de la mascota
        weight (Optional[float]): Nuevo peso de la mascota
        bloodType (Optional[str]): Nuevo tipo de sangre
        lastVaccination (Optional[str]): Nueva fecha de vacunación
        healthStatus (Optional[str]): Nuevo estado de salud
        petPhoto (UploadFile): Nueva foto de la mascota (opcional)
        db (AsyncIOMotorDatabase): Instancia de la base de datos
        current_user_id (str): ID del usuario autenticado (obtenido del token JWT)
    
    Returns:
        PetResponse: Mascota actualizada
        
    Raises:
        HTTPException: Si la mascota no existe, no pertenece al usuario o ocurre un error al actualizarla
    """
    try:
        # Verificar que la mascota existe y pertenece al usuario autenticado
        existing_pet = await PetMongoModel.get_pet_by_id(pet_id, db)
        if not existing_pet:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
        if existing_pet.ownerId != current_user_id:
            raise HTTPException(
                status_code=403, 
                detail="No tienes permisos para modificar esta mascota"
            )
        
        pet_data = PetUpdate(
            petName=petName,
            species=species,
            breed=breed,
            age=age,
            weight=weight,
            bloodType=bloodType,
            lastVaccination=lastVaccination,
            healthStatus=healthStatus
        )
        
        # Subir nueva imagen si se proporciona
        if petPhoto:
            try:
                # Generar un ID único para la nueva imagen
                photo_id = secrets.token_hex(12)
                photo_url = upload_image(petPhoto.file, public_id=photo_id)
                
                # Actualizar la foto en la base de datos
                pet = await PetMongoModel.update_pet_photo(pet_id, photo_url, db)
                if not pet:
                    raise HTTPException(status_code=404, detail="Mascota no encontrada")
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error al subir la imagen: {str(e)}"
                )
        
        # Actualizar otros datos de la mascota
        pet = await PetMongoModel.update_pet(pet_id, pet_data, db)
        if not pet:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
        return pet
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al actualizar la mascota"
        )

@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mascota",
    description="Elimina una mascota y su foto asociada de Cloudinary. Solo permite eliminar mascotas propias del usuario autenticado.",
    tags=["Mascotas"],
    responses={
        204: {
            "description": "Mascota eliminada exitosamente"
        },
        401: {
            "description": "Token de autorización requerido o inválido",
            "content": {
                "application/json": {
                    "example": {"detail": "Token de autorización requerido"}
                }
            }
        },
        403: {
            "description": "No autorizado para eliminar esta mascota",
            "content": {
                "application/json": {
                    "example": {"detail": "No tienes permisos para eliminar esta mascota"}
                }
            }
        },
        404: {
            "description": "Mascota no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Mascota no encontrada"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al eliminar la mascota"}
                }
            }
        }
    }
)
async def delete_pet_endpoint(
    pet_id: str, 
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Elimina una mascota y su foto asociada de Cloudinary.
    Solo permite eliminar mascotas propias del usuario autenticado.
    
    Args:
        pet_id (str): ID de la mascota a eliminar
        db (AsyncIOMotorDatabase): Instancia de la base de datos
        current_user_id (str): ID del usuario autenticado (obtenido del token JWT)
    
    Returns:
        None: Mascota eliminada exitosamente
        
    Raises:
        HTTPException: Si la mascota no existe, no pertenece al usuario o ocurre un error al eliminarla
    """
    try:
        # Obtener la mascota para verificar permisos y eliminar la foto de Cloudinary
        pet = await PetMongoModel.get_pet_by_id(pet_id, db)
        if not pet:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
        # Verificar que la mascota pertenece al usuario autenticado
        if pet.ownerId != current_user_id:
            raise HTTPException(
                status_code=403, 
                detail="No tienes permisos para eliminar esta mascota"
            )
        
        # Eliminar foto de Cloudinary si existe
        if pet.petPhoto:
            delete_image(pet.petPhoto)
        
        # Eliminar mascota de la base de datos
        deleted = await PetMongoModel.delete_pet(pet_id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al eliminar la mascota"
        )

@router.get(
    "/photo/{pet_id}",
    summary="Obtener foto de mascota",
    description="Redirige a la URL de la foto de la mascota almacenada en Cloudinary.",
    tags=["Mascotas"],
    responses={
        302: {
            "description": "Redirección a la foto de la mascota",
            "headers": {
                "Location": {
                    "description": "URL de la foto en Cloudinary",
                    "schema": {"type": "string", "example": "https://res.cloudinary.com/cloud_name/image/upload/v1234567890/mascotas/luna.jpg"}
                }
            }
        },
        404: {
            "description": "Mascota o foto no encontrada",
            "content": {
                "application/json": {
                    "example": {"detail": "Mascota no encontrada"}
                }
            }
        },
        500: {
            "description": "Error interno del servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Error interno del servidor al obtener la foto"}
                }
            }
        }
    }
)
async def get_pet_photo(pet_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Obtiene la foto de una mascota redirigiendo a la URL de Cloudinary.
    
    Args:
        pet_id (str): ID de la mascota
        db (AsyncIOMotorDatabase): Instancia de la base de datos
    
    Returns:
        RedirectResponse: Redirección a la URL de la foto
        
    Raises:
        HTTPException: Si la mascota no existe, no tiene foto o ocurre un error
    """
    try:
        pet = await PetMongoModel.get_pet_by_id(pet_id, db)
        if not pet:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")
        
        if not pet.petPhoto:
            raise HTTPException(status_code=404, detail="Foto no encontrada")
        
        # Redirigir a la URL de Cloudinary
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=pet.petPhoto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al obtener la foto"
        )
