import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect_to_mongo(cls):
        """
        Conecta a MongoDB usando las variables de entorno
        """
        try:
            # Usar siempre las variables de entorno
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            database_name = os.getenv("MONGODB_DATABASE", "mascotas")
            
            print(f"🔌 Conectando a MongoDB: {database_name}")
            
            # Crear cliente de MongoDB
            cls.client = AsyncIOMotorClient(mongodb_url)
            cls.database = cls.client[database_name]
            
            # Verificar conexión
            await cls.client.admin.command('ping')
            print("✅ Conectado a MongoDB exitosamente")
            
        except ConnectionFailure as e:
            print(f"❌ Error conectando a MongoDB: {str(e)}")
            raise
        except Exception as e:
            print(f"❌ Error inesperado conectando a MongoDB: {str(e)}")
            raise

    @classmethod
    async def close_mongo_connection(cls):
        """
        Cierra la conexión a MongoDB
        """
        if cls.client:
            cls.client.close()
            print("🔌 Conexión a MongoDB cerrada")

    @classmethod
    def get_database(cls):
        """
        Obtiene la base de datos de MongoDB
        """
        if cls.database is None:
            raise Exception("MongoDB no está conectado")
        return cls.database

    @classmethod
    def get_collection(cls, collection_name: str):
        """
        Obtiene una colección específica de MongoDB
        
        Args:
            collection_name (str): Nombre de la colección
            
        Returns:
            Collection: Colección de MongoDB
        """
        if cls.database is None:
            raise Exception("MongoDB no está conectado")
        return cls.database[collection_name]

# Instancia global
db = Database()

# Función de compatibilidad para mantener el código existente
async def get_database():
    return db.get_database() 