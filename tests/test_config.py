import os
from app.core.config import settings

# Configuración específica para testing
# Establecer modo testing explícitamente
os.environ["APP_ENV"] = "testing"
os.environ["DEBUG"] = "True"

print("✅ Configuración de testing cargada")

# Verificar variables críticas
mongodb_test_url = os.getenv("MONGODB_TEST_URL")
mongodb_test_database = os.getenv("MONGODB_TEST_DATABASE")

if mongodb_test_url and mongodb_test_database:
    print(f"📊 MongoDB Test URL: {mongodb_test_url}")
    print(f"📊 MongoDB Test Database: {mongodb_test_database}")
else:
    print("❌ ERROR: Variables de entorno de testing no configuradas")
    print("   MONGODB_TEST_URL: ", "✅" if mongodb_test_url else "❌")
    print("   MONGODB_TEST_DATABASE: ", "✅" if mongodb_test_database else "❌")
    print("   Asegúrate de que estas variables estén configuradas en tu archivo .env")
    raise Exception("Variables de entorno de testing no configuradas") 