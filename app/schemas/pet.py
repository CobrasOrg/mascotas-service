from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from app.core.enums import SpeciesEnum, BloodTypeEnum, BREEDS

class PetBase(BaseModel):
    petName: str = Field(..., example="Firulais")
    species: SpeciesEnum = Field(..., example="canine")
    breed: str = Field(..., example="Beagle")
    age: int = Field(..., ge=0, example=5)
    weight: float = Field(..., ge=0.1, example=12.5)
    bloodType: BloodTypeEnum = Field(..., example="DEA 1.1+")
    lastVaccination: date = Field(..., example="2025-07-01")
    healthStatus: str = Field(..., example="Sano y vacunado")

    @validator("breed")
    def validate_breed(cls, breed, values):
        species = values.get("species")
        if species and breed not in BREEDS[species]:
            raise ValueError(f"La raza '{breed}' no es válida para la especie '{species}'")
        return breed

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    petName: Optional[str] = Field(None, example="Max")
    species: Optional[SpeciesEnum] = Field(None, example="feline")
    breed: Optional[str] = Field(None, example="Siamés")
    age: Optional[int] = Field(None, example=4)
    weight: Optional[float] = Field(None, example=5.8)
    bloodType: Optional[BloodTypeEnum] = Field(None, example="A")
    lastVaccination: Optional[date] = Field(None, example="2025-06-01")
    healthStatus: Optional[str] = Field(None, example="Leve anemia, bajo control")

class PetResponse(PetBase):
    id: str = Field(..., example="d8a2f0b1-3542-4b92-9bb4-b14de55b08f6")
    petPhoto: Optional[str] = Field(None, example="/virtual/photo/d8a2f0b1-3542-4b92-9bb4-b14de55b08f6")
    ownerId: str = Field(..., example="user-123")
    registeredAt: str = Field(..., example="2025-07-11T12:00:00Z")
    updatedAt: str = Field(..., example="2025-07-11T12:00:00Z")