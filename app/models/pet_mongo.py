from datetime import datetime, time, date, UTC
from typing import List, Optional, Dict
from bson import ObjectId
from app.schemas.pet import PetCreate, PetUpdate, PetResponse
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

class PetMongoModel:
    collection_name = "mascotas"
    
    @staticmethod
    def get_collection(db: AsyncIOMotorDatabase):
        """Obtiene la colección de mascotas"""
        return db[PetMongoModel.collection_name]
    
    @staticmethod
    def _convert_mongo_doc_to_schema(doc: Dict) -> Dict:
        """Convierte un documento de MongoDB al formato del esquema Pydantic (PetResponse)"""
        if not doc:
            return doc
        # Convertir _id a id
        if "_id" in doc:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        # Convertir campos datetime a string ISO
        for field in ["registeredAt", "updatedAt", "lastVaccination"]:
            if field in doc and isinstance(doc[field], (datetime, date)):
                doc[field] = doc[field].isoformat()
        # Asegurar nombres de campo en camelCase
        # Si los datos vienen en snake_case, convertirlos
        mapping = {
            "pet_name": "petName",
            "species": "species",
            "breed": "breed",
            "age": "age",
            "weight": "weight",
            "blood_type": "bloodType",
            "last_vaccination": "lastVaccination",
            "health_status": "healthStatus",
            "pet_photo": "petPhoto",
            "owner_id": "ownerId",
            "registered_at": "registeredAt",
            "updated_at": "updatedAt"
        }
        for old, new in mapping.items():
            if old in doc:
                doc[new] = doc.pop(old)
        return doc
    
    @staticmethod
    async def get_pets_by_owner(owner_id: str, db: AsyncIOMotorDatabase) -> List[PetResponse]:
        """
        Get all pets by owner from MongoDB
        Args:
            owner_id (str): ID of the owner
            db (AsyncIOMotorDatabase): Database connection
        Returns:
            List[PetResponse]: List of pets for the owner
        """
        try:
            collection = PetMongoModel.get_collection(db)
            cursor = collection.find({"ownerId": owner_id})
            pets = await cursor.to_list(length=None)
            
            print(f"🔍 Encontradas {len(pets)} mascotas para owner_id: {owner_id}")
            if pets:
                print(f"🔍 Primera mascota en DB: {pets[0]}")
            
            converted_pets = []
            for pet in pets:
                try:
                    converted_pet = PetMongoModel._convert_mongo_doc_to_schema(pet)
                    print(f"🔍 Mascota convertida: {converted_pet}")
                    pet_response = PetResponse(**converted_pet)
                    converted_pets.append(pet_response)
                except Exception as e:
                    print(f"❌ Error convirtiendo mascota: {e}")
                    print(f"🔍 Datos de la mascota: {pet}")
                    continue
            
            return converted_pets
        except Exception as e:
            print(f"❌ Error en get_pets_by_owner: {e}")
            return []

    @staticmethod
    async def create_pet(pet_data: PetCreate, owner_id: str, db: AsyncIOMotorDatabase, photo_url: str = None) -> PetResponse:
        """
        Create a new pet in MongoDB
        Args:
            pet_data (PetCreate): Pet data
            owner_id (str): ID of the owner
            db (AsyncIOMotorDatabase): Database connection
            photo_url (str): URL of the pet photo (optional)
        Returns:
            PetResponse: Created pet
        """
        collection = PetMongoModel.get_collection(db)
        
        # Crear documento para insertar
        pet_dict = pet_data.model_dump()
        
        # Convertir datetime.date a datetime.datetime para MongoDB
        if 'lastVaccination' in pet_dict and isinstance(pet_dict['lastVaccination'], date):
            pet_dict['lastVaccination'] = datetime.combine(pet_dict['lastVaccination'], time.min)
        
        pet_dict.update({
            "ownerId": owner_id,
            "registeredAt": datetime.now(UTC).isoformat(),
            "updatedAt": datetime.now(UTC).isoformat(),
            "petPhoto": photo_url
        })
        
        result = await collection.insert_one(pet_dict)
        
        # Obtener el documento insertado
        inserted_doc = await collection.find_one({"_id": result.inserted_id})
        
        # Convertir ObjectId a string para el esquema
        converted_doc = PetMongoModel._convert_mongo_doc_to_schema(inserted_doc)
        
        return PetResponse(**converted_doc)

    @staticmethod
    async def update_pet(pet_id: str, pet_data: PetUpdate, db: AsyncIOMotorDatabase) -> Optional[PetResponse]:
        """
        Update pet data in MongoDB
        Args:
            pet_id (str): ID of the pet
            pet_data (PetUpdate): Updated pet data
            db (AsyncIOMotorDatabase): Database connection
        Returns:
            Optional[PetResponse]: Updated pet if found, None otherwise
        """
        collection = PetMongoModel.get_collection(db)
        
        try:
            object_id = ObjectId(pet_id)
            
            # First, get the existing pet to ensure it exists
            existing_doc = await collection.find_one({"_id": object_id})
            if not existing_doc:
                return None
            
            # Prepare update data
            update_data = pet_data.model_dump(exclude_unset=True)
            # Filter out None values to avoid overwriting existing data
            update_data = {k: v for k, v in update_data.items() if v is not None}
            update_data["updatedAt"] = datetime.now(UTC)
            
            result = await collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                # Obtener el documento actualizado
                updated_doc = await collection.find_one({"_id": object_id})
                if updated_doc:
                    converted_doc = PetMongoModel._convert_mongo_doc_to_schema(updated_doc)
                    return PetResponse(**converted_doc)
            
            return None
        except Exception as e:
            print(f"❌ Error en update_pet: {e}")
            return None

    @staticmethod
    async def update_pet_photo(pet_id: str, photo_url: str, db: AsyncIOMotorDatabase) -> Optional[PetResponse]:
        """
        Update pet photo URL in MongoDB
        Args:
            pet_id (str): ID of the pet
            photo_url (str): New photo URL
            db (AsyncIOMotorDatabase): Database connection
        Returns:
            Optional[PetResponse]: Updated pet if found, None otherwise
        """
        collection = PetMongoModel.get_collection(db)
        
        try:
            object_id = ObjectId(pet_id)
            result = await collection.update_one(
                {"_id": object_id},
                {"$set": {"petPhoto": photo_url, "updatedAt": datetime.now(UTC)}}
            )
            
            if result.modified_count > 0:
                # Obtener el documento actualizado
                updated_doc = await collection.find_one({"_id": object_id})
                if updated_doc:
                    converted_doc = PetMongoModel._convert_mongo_doc_to_schema(updated_doc)
                    return PetResponse(**converted_doc)
            
            return None
        except Exception:
            return None

    @staticmethod
    async def delete_pet(pet_id: str, db: AsyncIOMotorDatabase) -> bool:
        """
        Delete a pet by ID from MongoDB
        Args:
            pet_id (str): ID of the pet to delete
            db (AsyncIOMotorDatabase): Database connection
        Returns:
            bool: True if deleted, False if not found
        """
        collection = PetMongoModel.get_collection(db)
        
        try:
            object_id = ObjectId(pet_id)
            result = await collection.delete_one({"_id": object_id})
            return result.deleted_count > 0
        except Exception:
            return False

    @staticmethod
    async def get_pet_by_id(pet_id: str, db: AsyncIOMotorDatabase) -> Optional[PetResponse]:
        """
        Get a pet by ID from MongoDB
        Args:
            pet_id (str): ID of the pet
            db (AsyncIOMotorDatabase): Database connection
        Returns:
            Optional[PetResponse]: Pet if found, None otherwise
        """
        collection = PetMongoModel.get_collection(db)
        
        try:
            object_id = ObjectId(pet_id)
            pet = await collection.find_one({"_id": object_id})
            
            if pet:
                converted_doc = PetMongoModel._convert_mongo_doc_to_schema(pet)
                return PetResponse(**converted_doc)
            
            return None
        except Exception:
            return None 