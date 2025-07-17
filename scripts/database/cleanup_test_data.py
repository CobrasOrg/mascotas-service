#!/usr/bin/env python3
"""
Script para limpiar datos de prueba de la base de datos de testing
Uso: python cleanup_test_data.py
"""

import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Cargar variables de entorno
load_dotenv()

async def cleanup_test_database():
    """Limpia la base de datos de testing y elimina imágenes de Cloudinary"""
    test_url = os.getenv("MONGODB_TEST_URL")
    test_database = os.getenv("MONGODB_TEST_DATABASE")
    if not test_url or not test_database:
        print("⚠️ Variables de entorno de testing no configuradas")
        print("   MONGODB_TEST_URL y MONGODB_TEST_DATABASE no están definidas")
        return
    print(f"🧪 Limpiando base de datos de testing: {test_database}")
    try:
        client = AsyncIOMotorClient(test_url)
        db = client[test_database]
        await client.admin.command('ping')
        print("✅ Conexión exitosa a base de datos de testing")
        collections = await db.list_collection_names()
        print(f"📋 Colecciones en testing: {collections}")
        total_deleted = 0
        images_deleted = 0
        for collection_name in collections:
            count_before = await db[collection_name].count_documents({})
            if count_before > 0:
                # Si es la colección de mascotas, eliminar imágenes de Cloudinary primero
                if collection_name == "mascotas":
                    print(f"🖼️ Eliminando imágenes de Cloudinary para {count_before} mascotas...")
                    mascotas = await db[collection_name].find({}).to_list(length=None)
                    for mascota in mascotas:
                        if "petPhoto" in mascota and mascota["petPhoto"]:
                            try:
                                from app.services.cloudinary_service import delete_image
                                if delete_image(mascota["petPhoto"]):
                                    images_deleted += 1
                                    print(f"✅ Imagen eliminada: {mascota['petName']}")
                                else:
                                    print(f"⚠️ No se pudo eliminar imagen: {mascota['petName']}")
                            except Exception as img_error:
                                print(f"❌ Error eliminando imagen de {mascota['petName']}: {img_error}")
                # Eliminar todos los documentos
                result = await db[collection_name].delete_many({})
                deleted_count = result.deleted_count
                total_deleted += deleted_count
                print(f"🗑️ Testing '{collection_name}': {count_before} → {deleted_count} eliminados")
            else:
                print(f"✅ Testing '{collection_name}': ya está vacía")
        # Verificar limpieza
        total_remaining = 0
        for collection_name in collections:
            count_after = await db[collection_name].count_documents({})
            total_remaining += count_after
        if total_remaining == 0:
            print(f"✅ Limpieza de testing completada:")
            print(f"   📊 {total_deleted} documentos eliminados")
            print(f"   🖼️ {images_deleted} imágenes de Cloudinary eliminadas")
        else:
            print(f"❌ ERROR: {total_remaining} documentos permanecen en testing")
        client.close()
        print("🔌 Conexión de testing cerrada")
    except Exception as e:
        print(f"❌ Error durante la limpieza de testing: {str(e)}")
        try:
            client.close()
        except:
            pass

async def main():
    print("🧹 Iniciando limpieza de datos de prueba de testing...")
    print("=" * 50)
    print("\n🧪 LIMPIEZA DE BASE DE DATOS DE TESTING")
    print("-" * 40)
    await cleanup_test_database()
    print("\n" + "=" * 50)
    print("✅ Proceso de limpieza de testing completado")

if __name__ == "__main__":
    asyncio.run(main()) 