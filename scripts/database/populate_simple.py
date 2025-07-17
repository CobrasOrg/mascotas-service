#!/usr/bin/env python3
"""
Script simple para poblar la base de datos con datos básicos (sin imágenes)
Uso: python populate_simple.py
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.pet_mongo import PetMongoModel
from app.schemas.pet import PetCreate

# Cargar variables de entorno
load_dotenv()

# Datos de ejemplo para mascotas (sin imágenes)
SAMPLE_PETS_SIMPLE = [
    {
        "petName": "Luna",
        "species": "feline",
        "breed": "Siamés",
        "age": 3,
        "weight": 4.5,
        "bloodType": "A",
        "lastVaccination": "2024-01-15",
        "healthStatus": "Saludable",
        "ownerId": "user-123"
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
        "ownerId": "user-123"
    },
    {
        "petName": "Bella",
        "species": "canine",
        "breed": "Labrador",
        "age": 2,
        "weight": 22.5,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-03-10",
        "healthStatus": "Saludable",
        "ownerId": "user-456"
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
        "ownerId": "user-456"
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
        "ownerId": "user-789"
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
        "ownerId": "user-789"
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
        "ownerId": "user-123"
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
        "ownerId": "user-456"
    },
    {
        "petName": "Charlie",
        "species": "canine",
        "breed": "Poodle",
        "age": 3,
        "weight": 12.0,
        "bloodType": "DEA 1.1+",
        "lastVaccination": "2024-02-10",
        "healthStatus": "Saludable",
        "ownerId": "user-789"
    },
    {
        "petName": "Fluffy",
        "species": "feline",
        "breed": "British Shorthair",
        "age": 5,
        "weight": 7.5,
        "bloodType": "A",
        "lastVaccination": "2024-01-25",
        "healthStatus": "Saludable",
        "ownerId": "user-123"
    }
]

async def create_simple_pet(pet_data: dict, db) -> bool:
    """
    Crea una mascota simple en la base de datos (sin imagen)
    
    Args:
        pet_data: Datos de la mascota
        db: Instancia de la base de datos
        
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
        
        # Crear la mascota en la base de datos (sin imagen)
        pet = await PetMongoModel.create_pet(
            pet_create, 
            pet_data["ownerId"], 
            db, 
            None  # Sin imagen
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

async def populate_database_simple():
    """Puebla la base de datos con datos básicos (sin imágenes)"""
    
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
        print("\n🐾 Creando mascotas de ejemplo (sin imágenes)...")
        successful_creations = 0
        
        for i, pet_data in enumerate(SAMPLE_PETS_SIMPLE, 1):
            print(f"\n[{i}/{len(SAMPLE_PETS_SIMPLE)}] Procesando: {pet_data['petName']}")
            
            success = await create_simple_pet(pet_data, db)
            if success:
                successful_creations += 1
            
            # Pequeña pausa entre creaciones
            await asyncio.sleep(0.2)
        
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
                print(f"   • {pet['petName']} ({pet['species']}) - {pet['breed']} - Propietario: {pet['ownerId']}")
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

async def populate_test_database_simple():
    """Puebla la base de datos de testing con datos básicos"""
    
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
        
        # Crear algunas mascotas de prueba
        test_pets = SAMPLE_PETS_SIMPLE[:5]  # Solo las primeras 5 para testing
        
        print(f"\n🐾 Creando {len(test_pets)} mascotas de prueba...")
        successful_creations = 0
        
        for i, pet_data in enumerate(test_pets, 1):
            print(f"\n[{i}/{len(test_pets)}] Procesando: {pet_data['petName']}")
            
            success = await create_simple_pet(pet_data, db)
            if success:
                successful_creations += 1
            
            await asyncio.sleep(0.1)  # Pausa muy corta para testing
        
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
    print("🐾 Iniciando población simple de base de datos...")
    print("=" * 50)
    
    # Poblar base de datos principal
    print("\n📊 POBLACIÓN DE BASE DE DATOS PRINCIPAL")
    print("-" * 40)
    await populate_database_simple()
    
    # Poblar base de datos de testing
    print("\n🧪 POBLACIÓN DE BASE DE DATOS DE TESTING")
    print("-" * 40)
    await populate_test_database_simple()
    
    print("\n" + "=" * 50)
    print("✅ Proceso de población simple completado")

if __name__ == "__main__":
    asyncio.run(main()) 