from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.storage.memory import DB, PHOTO_STORE
from uuid import uuid4
from datetime import datetime, UTC
from fastapi import UploadFile, HTTPException
from typing import Optional


def get_pets_by_owner(owner_id: str) -> list[PetResponse]:
    return [PetResponse(**pet) for pet in DB.values() if pet["ownerId"] == owner_id]


def delete_pet(pet_id: str):
    if pet_id not in DB:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    del DB[pet_id]

def create_pet(data: PetCreate, petPhoto: Optional[UploadFile]) -> PetResponse:
    pet_id = str(uuid4())
    now = datetime.now(UTC).isoformat()
    pet_dict = data.dict()

    if petPhoto:
        content = petPhoto.file.read()
        PHOTO_STORE[pet_id] = content
        photo_url = f"/virtual/photo/{pet_id}"
    else:
        photo_url = None

    pet_dict.update({
        "id": pet_id,
        "ownerId": "demo_owner",
        "registeredAt": now,
        "updatedAt": now,
        "petPhoto": photo_url
    })
    DB[pet_id] = pet_dict
    return PetResponse(**pet_dict)

def update_pet(pet_id: str, data: PetUpdate, petPhoto: Optional[UploadFile]) -> PetResponse:
    if pet_id not in DB:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    pet = DB[pet_id]
    update_data = data.dict(exclude_unset=True)
    pet.update(update_data)
    pet["updatedAt"] = datetime.now(UTC).isoformat()

    if petPhoto:
        content = petPhoto.file.read()
        PHOTO_STORE[pet_id] = content
        pet["petPhoto"] = f"/virtual/photo/{pet_id}"

    DB[pet_id] = pet
    return PetResponse(**pet)