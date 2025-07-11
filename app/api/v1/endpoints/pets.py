from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List, Optional
from app.storage.memory import DB, PHOTO_STORE
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.services.pet_service import (
    create_pet,
    get_pets_by_owner,
    update_pet,
    delete_pet
)

router = APIRouter()

@router.get("/", response_model=List[PetResponse])
def list_pets(owner_id: str = "demo_owner"):
    return get_pets_by_owner(owner_id)

@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet_endpoint(
    petName: str = Form(...),
    species: str = Form(...),
    breed: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    bloodType: str = Form(...),
    lastVaccination: str = Form(...),
    healthStatus: str = Form(...),
    petPhoto: Optional[UploadFile] = File(None),
):
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
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return create_pet(pet_data, petPhoto)

@router.put("/{pet_id}", response_model=PetResponse)
def update_pet_endpoint(
    pet_id: str,
    petName: Optional[str] = Form(None),
    species: Optional[str] = Form(None),
    breed: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    weight: Optional[float] = Form(None),
    bloodType: Optional[str] = Form(None),
    lastVaccination: Optional[str] = Form(None),
    healthStatus: Optional[str] = Form(None),
    petPhoto: Optional[UploadFile] = File(None),
):
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
    return update_pet(pet_id, pet_data, petPhoto)

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_endpoint(pet_id: str):
    delete_pet(pet_id)
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List, Optional
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.services.pet_service import (
    create_pet,
    get_pets_by_owner,
    update_pet,
    delete_pet
)

router = APIRouter()

@router.get("/", response_model=List[PetResponse])
def list_pets(owner_id: str = "demo_owner"):
    return get_pets_by_owner(owner_id)

@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet_endpoint(
    petName: str = Form(...),
    species: str = Form(...),
    breed: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    bloodType: str = Form(...),
    lastVaccination: str = Form(...),
    healthStatus: str = Form(...),
    petPhoto: Optional[UploadFile] = File(None),
):
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
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return create_pet(pet_data, petPhoto)

@router.put("/{pet_id}", response_model=PetResponse)
def update_pet_endpoint(
    pet_id: str,
    petName: Optional[str] = Form(None),
    species: Optional[str] = Form(None),
    breed: Optional[str] = Form(None),
    age: Optional[int] = Form(None),
    weight: Optional[float] = Form(None),
    bloodType: Optional[str] = Form(None),
    lastVaccination: Optional[str] = Form(None),
    healthStatus: Optional[str] = Form(None),
    petPhoto: Optional[UploadFile] = File(None),
):
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
    return update_pet(pet_id, pet_data, petPhoto)

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_endpoint(pet_id: str):
    delete_pet(pet_id)

@router.get("/photo/{pet_id}")
def get_pet_photo(pet_id: str):
    photo = PHOTO_STORE.get(pet_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return StreamingResponse(iter([photo]), media_type="image/jpeg")