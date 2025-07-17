#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo
Uso: python populate_database.py
"""

import asyncio
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.pet_mongo import PetMongoModel
from app.schemas.pet import PetCreate
from app.services.cloudinary_service import upload_image
from app.core.enums import SpeciesEnum, BloodTypeEnum

# Cargar variables de entorno
load_dotenv()

# Datos de ejemplo para mascotas
SAMPLE_PETS = [
    {
        "petName": "Luna",
        "species": "feline",
        "breed": "Siamés",
        "age": 3,
        "weight": 4.5,
        "bloodType": "A",
        "lastVaccination": "2024-01-15",
        "healthStatus": "Saludable",
        "ownerId": "user-123",
        "image_file": "gato.jpeg"
    },
    {
        "petName": "Max",
        "species": "canine",
        "breed": "Golden Retriever",
        "age": 5,
        "weight": 25.0,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-02-20",
        "healthStatus": "Saludable",
        "ownerId": "user-123",
        "image_file": "perro.jpeg"
    },
    {
        "petName": "Bella",
        "species": "canine",
        "breed": "Labrador Retriever",
        "age": 2,
        "weight": 22.5,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-03-10",
        "healthStatus": "Saludable",
        "ownerId": "user-456",
        "image_file": "perro.jpeg"
    },
    {
        "petName": "Mittens",
        "species": "feline",
        "breed": "Persa",
        "age": 4,
        "weight": 5.2,
        "bloodType": "A",
        "lastVaccination": "2024-01-30",
        "healthStatus": "Saludable",
        "ownerId": "user-456",
        "image_file": "gato.jpeg"
    },
    {
        "petName": "Rocky",
        "species": "canine",
        "breed": "Pastor Alemán",
        "age": 6,
        "weight": 30.0,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-02-15",
        "healthStatus": "Saludable",
        "ownerId": "user-789",
        "image_file": "perro.jpeg"
    },
    {
        "petName": "Shadow",
        "species": "feline",
        "breed": "Maine Coon",
        "age": 2,
        "weight": 6.8,
        "bloodType": "A",
        "lastVaccination": "2024-03-05",
        "healthStatus": "Saludable",
        "ownerId": "user-789",
        "image_file": "gato.jpeg"
    },
    {
        "petName": "Buddy",
        "species": "canine",
        "breed": "Beagle",
        "age": 4,
        "weight": 18.5,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-01-20",
        "healthStatus": "Saludable",
        "ownerId": "user-123",
        "image_file": "perro.jpeg"
    },
    {
        "petName": "Whiskers",
        "species": "feline",
        "breed": "Ragdoll",
        "age": 1,
        "weight": 3.2,
        "bloodType": "A",
        "lastVaccination": "2024-04-01",
        "healthStatus": "Saludable",
        "ownerId": "user-456",
        "image_file": "gato.jpeg"
    }
]

async def upload_image_to_cloudinary(image_path: str, pet_name: str) -> str:
    """
    Sube una imagen a Cloudinary y retorna la URL
    
    Args:
        image_path: Ruta de la imagen
        pet_name: Nombre de la mascota para el ID público
        
    Returns:
        str: URL de la imagen en Cloudinary
    """
    try:
        with open(image_path, "rb") as image_file:
            # Generar ID único para la imagen
            public_id = f"mascotas/{pet_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            url = upload_image(image_file, public_id=public_id)
            print(f"✅ Imagen subida para {pet_name}: {url}")
            return url
    except Exception as e:
        print(f"❌ Error subiendo imagen para {pet_name}: {e}")
        return None

async def create_pet_with_image(pet_data: dict, db, images_dir: str) -> bool:
    """
    Crea una mascota con imagen en la base de datos
    
    Args:
        pet_data: Datos de la mascota
        db: Instancia de la base de datos
        images_dir: Directorio de imágenes
        
    Returns:
        bool: True si se creó exitosamente
    """
    try:
        # Preparar datos de la mascota
        pet_create = PetCreate(
            petName=pet_data["petName"],
            species=pet_data["species"],
            breed=pet_data["breed"],
            age=pet_data["age"],
            weight=pet_data["weight"],
            bloodType=pet_data["bloodType"],
            lastVaccination=pet_data["lastVaccination"],
            healthStatus=pet_data["healthStatus"]
        )
        
        # Subir imagen si existe
        photo_url = None
        image_file = pet_data.get("image_file")
        if image_file:
            image_path = os.path.join(images_dir, image_file)
            if os.path.exists(image_path):
                photo_url = await upload_image_to_cloudinary(image_path, pet_data["petName"])
        
        # Crear la mascota en la base de datos
        pet = await PetMongoModel.create_pet(
            pet_create, 
            pet_data["ownerId"], 
            db, 
            photo_url
        )
        
        if pet:
            print(f"✅ Mascota creada: {pet_data['petName']} (ID: {pet.id})")
            return True
        else:
            print(f"❌ Error creando mascota: {pet_data['petName']}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando mascota {pet_data['petName']}: {e}")
        return False

async def populate_database():
    """Puebla la base de datos con datos de ejemplo"""
    
    # Obtener configuración de la base de datos
    mongodb_url = os.getenv("MONGODB_URL")
    mongodb_database = os.getenv("MONGODB_DATABASE")
    
    if not mongodb_url or not mongodb_database:
        print("❌ Variables de entorno MONGODB_URL y MONGODB_DATABASE no configuradas")
        return
    
    print(f"🔍 Conectando a: {mongodb_url}")
    print(f"📊 Base de datos: {mongodb_database}")
    
    try:
        # Conectar a MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[mongodb_database]
        
        # Verificar conexión
        await client.admin.command('ping')
        print("✅ Conexión exitosa a MongoDB")
        
        # Verificar directorio de imágenes
        images_dir = os.path.join("app", "data", "images")
        if not os.path.exists(images_dir):
            print(f"❌ Directorio de imágenes no encontrado: {images_dir}")
            return
        
        print(f"📁 Directorio de imágenes: {images_dir}")
        
        # Verificar archivos de imagen
        image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        print(f"🖼️ Imágenes disponibles: {image_files}")
        
        # Contar mascotas existentes
        existing_pets = await db["mascotas"].count_documents({})
        print(f"📊 Mascotas existentes: {existing_pets}")
        
        if existing_pets > 0:
            print("⚠️ Ya existen mascotas en la base de datos")
            response = input("¿Deseas continuar y agregar más mascotas? (y/N): ")
            if response.lower() != 'y':
                print("❌ Operación cancelada")
                return
        
        # Crear mascotas de ejemplo
        print("\n🐾 Creando mascotas de ejemplo...")
        successful_creations = 0
        
        for i, pet_data in enumerate(SAMPLE_PETS, 1):
            print(f"\n[{i}/{len(SAMPLE_PETS)}] Procesando: {pet_data['petName']}")
            
            success = await create_pet_with_image(pet_data, db, images_dir)
            if success:
                successful_creations += 1
            
            # Pequeña pausa entre creaciones para no sobrecargar Cloudinary
            await asyncio.sleep(1)
        
        # Verificar resultados
        total_pets = await db["mascotas"].count_documents({})
        print(f"\n📊 Resumen:")
        print(f"   ✅ Mascotas creadas exitosamente: {successful_creations}")
        print(f"   📈 Total de mascotas en la base de datos: {total_pets}")
        
        if successful_creations > 0:
            print("\n🎉 Base de datos poblada exitosamente!")
            print("\n📋 Mascotas creadas:")
            pets = await db["mascotas"].find({}).to_list(None)
            for pet in pets:
                print(f"   • {pet['petName']} ({pet['species']}) - {pet['breed']}")
        else:
            print("\n❌ No se pudo crear ninguna mascota")
        
        # Cerrar conexión
        client.close()
        print("🔌 Conexión cerrada")
        
    except Exception as e:
        print(f"❌ Error durante la población: {str(e)}")
        try:
            client.close()
        except:
            pass

async def populate_test_database():
    """Puebla la base de datos de testing con datos de ejemplo"""
    
    # Obtener configuración de testing
    test_url = os.getenv("MONGODB_TEST_URL")
    test_database = os.getenv("MONGODB_TEST_DATABASE")
    
    if not test_url or not test_database:
        print("⚠️ Variables de entorno de testing no configuradas")
        print("   MONGODB_TEST_URL y MONGODB_TEST_DATABASE no están definidas")
        return
    
    print(f"🧪 Poblando base de datos de testing: {test_database}")
    
    try:
        # Conectar a la base de datos de testing
        client = AsyncIOMotorClient(test_url)
        db = client[test_database]
        
        # Verificar conexión
        await client.admin.command('ping')
        print("✅ Conexión exitosa a base de datos de testing")
        
        # Verificar directorio de imágenes
        images_dir = os.path.join("app", "data", "images")
        if not os.path.exists(images_dir):
            print(f"❌ Directorio de imágenes no encontrado: {images_dir}")
            return
        
        # Crear algunas mascotas de prueba
        test_pets = SAMPLE_PETS[:3]  # Solo las primeras 3 para testing
        
        print(f"\n🐾 Creando {len(test_pets)} mascotas de prueba...")
        successful_creations = 0
        
        for i, pet_data in enumerate(test_pets, 1):
            print(f"\n[{i}/{len(test_pets)}] Procesando: {pet_data['petName']}")
            
            success = await create_pet_with_image(pet_data, db, images_dir)
            if success:
                successful_creations += 1
            
            await asyncio.sleep(0.5)  # Pausa más corta para testing
        
        # Verificar resultados
        total_pets = await db["mascotas"].count_documents({})
        print(f"\n📊 Resumen de testing:")
        print(f"   ✅ Mascotas creadas: {successful_creations}")
        print(f"   📈 Total en testing: {total_pets}")
        
        # Cerrar conexión
        client.close()
        print("🔌 Conexión de testing cerrada")
        
    except Exception as e:
        print(f"❌ Error durante la población de testing: {str(e)}")
        try:
            client.close()
        except:
            pass

async def main():
    """Función principal"""
    print("🐾 Iniciando población de base de datos de testing...")
    print("=" * 50)
    
    # Solo poblar base de datos de testing
    print("\n🧪 POBLACIÓN DE BASE DE DATOS DE TESTING")
    print("-" * 40)
    await populate_test_database()
    
    print("\n" + "=" * 50)
    print("✅ Proceso de población de testing completado")

if __name__ == "__main__":
    asyncio.run(main()) 