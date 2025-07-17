from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from app.core.enums import SpeciesEnum, BloodTypeEnum, BREEDS

class PetBase(BaseModel):
    petName: str = Field(..., json_schema_extra={"example": "Firulais"})
    species: SpeciesEnum = Field(..., json_schema_extra={"example": "canine"})
    breed: str = Field(..., json_schema_extra={"example": "Beagle"})
    age: int = Field(..., ge=0, json_schema_extra={"example": 5})
    weight: float = Field(..., ge=0.1, json_schema_extra={"example": 12.5})
    bloodType: BloodTypeEnum = Field(..., json_schema_extra={"example": "DEA 1.1+"})
    lastVaccination: date = Field(..., json_schema_extra={"example": "2025-07-01"})
    healthStatus: str = Field(..., json_schema_extra={"example": "Sano y vacunado"})

    @field_validator("breed")
    @classmethod
    def validate_breed(cls, breed, info):
        species = info.data.get("species")
        if species and breed not in BREEDS[species]:
            raise ValueError(f"La raza '{breed}' no es válida para la especie '{species}'")
        return breed

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    petName: Optional[str] = Field(None, json_schema_extra={"example": "Max"})
    species: Optional[SpeciesEnum] = Field(None, json_schema_extra={"example": "feline"})
    breed: Optional[str] = Field(None, json_schema_extra={"example": "Siamés"})
    age: Optional[int] = Field(None, json_schema_extra={"example": 4})
    weight: Optional[float] = Field(None, json_schema_extra={"example": 5.8})
    bloodType: Optional[BloodTypeEnum] = Field(None, json_schema_extra={"example": "A"})
    lastVaccination: Optional[date] = Field(None, json_schema_extra={"example": "2025-06-01"})
    healthStatus: Optional[str] = Field(None, json_schema_extra={"example": "Leve anemia, bajo control"})

class PetResponse(PetBase):
    id: str = Field(..., json_schema_extra={"example": "d8a2f0b1-3542-4b92-9bb4-b14de55b08f6"})
    petPhoto: Optional[str] = Field(None, json_schema_extra={"example": "/virtual/photo/d8a2f0b1-3542-4b92-9bb4-b14de55b08f6"})
    ownerId: str = Field(..., json_schema_extra={"example": "user-123"})
    registeredAt: str = Field(..., json_schema_extra={"example": "2025-07-11T12:00:00Z"})
    updatedAt: str = Field(..., json_schema_extra={"example": "2025-07-11T12:00:00Z"})