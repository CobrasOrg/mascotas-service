# Scripts de Base de Datos

Este directorio contiene scripts útiles para gestionar la base de datos del proyecto Mascotas Service.

## 📁 Scripts Disponibles

### 1. `cleanup_test_data.py` - Limpieza de Datos
**Propósito**: Elimina todos los datos de prueba de la base de datos.

**Uso**:
```bash
python cleanup_test_data.py
```

**Funcionalidades**:
- ✅ Limpia la base de datos principal
- ✅ Limpia la base de datos de testing
- ✅ Elimina imágenes de Cloudinary asociadas
- ✅ Verifica que la limpieza fue exitosa
- ✅ Manejo de errores robusto

**Cuándo usar**:
- Después de ejecutar pruebas
- Cuando hay datos residuales de testing
- Para limpiar datos de desarrollo

---

### 2. `populate_database.py` - Población con Imágenes
**Propósito**: Puebla la base de datos con datos de ejemplo incluyendo imágenes.

**Uso**:
```bash
python populate_database.py
```

**Funcionalidades**:
- ✅ Crea 8 mascotas de ejemplo
- ✅ Sube imágenes a Cloudinary
- ✅ Asocia mascotas con diferentes usuarios
- ✅ Puebla tanto base principal como testing
- ✅ Manejo de errores de Cloudinary

**Requisitos**:
- Variables de entorno de Cloudinary configuradas
- Imágenes disponibles en `app/data/images/`
- Conexión a MongoDB

**Datos creados**:
- **Luna** (Gato Siamés) - user-123
- **Max** (Perro Golden Retriever) - user-123
- **Bella** (Perro Labrador) - user-456
- **Mittens** (Gato Persa) - user-456
- **Rocky** (Perro Pastor Alemán) - user-789
- **Shadow** (Gato Maine Coon) - user-789
- **Buddy** (Perro Beagle) - user-123
- **Whiskers** (Gato Ragdoll) - user-456

---

### 3. `populate_simple.py` - Población Básica
**Propósito**: Puebla la base de datos con datos básicos (sin imágenes).

**Uso**:
```bash
python populate_simple.py
```

**Funcionalidades**:
- ✅ Crea 10 mascotas de ejemplo
- ✅ No requiere Cloudinary
- ✅ Más rápido y confiable
- ✅ Puebla tanto base principal como testing

**Cuándo usar**:
- Cuando Cloudinary no está disponible
- Para pruebas rápidas
- Cuando solo necesitas datos básicos

**Datos creados**:
- **Luna** (Gato Siamés) - user-123
- **Max** (Perro Golden Retriever) - user-123
- **Bella** (Perro Labrador) - user-456
- **Mittens** (Gato Persa) - user-456
- **Rocky** (Perro Pastor Alemán) - user-789
- **Shadow** (Gato Maine Coon) - user-789
- **Buddy** (Perro Beagle) - user-123
- **Whiskers** (Gato Ragdoll) - user-456
- **Charlie** (Perro Poodle) - user-789
- **Fluffy** (Gato British Shorthair) - user-123

---

## 🔧 Configuración Requerida

### Variables de Entorno

**Para base de datos principal**:
```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=mascotas
```

**Para base de datos de testing**:
```env
MONGODB_TEST_URL=mongodb://localhost:27017
MONGODB_TEST_DATABASE=mascotas_test
```

**Para Cloudinary (solo populate_database.py)**:
```env
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

---

## 📋 Flujo de Trabajo Recomendado

### 1. Desarrollo Inicial
```bash
# 1. Limpiar cualquier dato residual
python cleanup_test_data.py

# 2. Poblar con datos básicos
python populate_simple.py

# 3. Probar la API
curl -X GET "http://localhost:8000/api/v1/pets/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
```

### 2. Testing Completo
```bash
# 1. Limpiar datos
python cleanup_test_data.py

# 2. Ejecutar pruebas
pytest tests/ -v

# 3. Limpiar después de pruebas
python cleanup_test_data.py
```

### 3. Demostración con Imágenes
```bash
# 1. Limpiar datos
python cleanup_test_data.py

# 2. Poblar con imágenes
python populate_database.py

# 3. Probar endpoints con imágenes
curl -X GET "http://localhost:8000/api/v1/pets/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
```

---

## 🐛 Troubleshooting

### Error: "Variables de entorno no configuradas"
**Solución**: Verifica que tu archivo `.env` tenga todas las variables requeridas.

### Error: "Conexión a MongoDB fallida"
**Solución**: 
- Verifica que MongoDB esté ejecutándose
- Revisa la URL de conexión
- Asegúrate de que las credenciales sean correctas

### Error: "Cloudinary no configurado"
**Solución**: 
- Usa `populate_simple.py` en lugar de `populate_database.py`
- O configura las variables de Cloudinary

### Error: "Directorio de imágenes no encontrado"
**Solución**: 
- Verifica que exista `app/data/images/`
- Asegúrate de que las imágenes estén en el directorio correcto

### Datos que no se limpian
**Solución**:
```bash
# Ejecutar limpieza manual
python cleanup_test_data.py

# Si persisten, verificar conexión
python -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client[os.getenv('MONGODB_DATABASE')]

async def check():
    await client.admin.command('ping')
    count = await db['mascotas'].count_documents({})
    print(f'Mascotas en BD: {count}')
    await client.close()

asyncio.run(check())
"
```

---

## 📊 Monitoreo

### Verificar datos en la base de datos
```bash
# Conectar a MongoDB
mongosh

# Cambiar a la base de datos
use mascotas

# Contar mascotas
db.mascotas.countDocuments()

# Ver todas las mascotas
db.mascotas.find().pretty()

# Ver mascotas por usuario
db.mascotas.find({"ownerId": "user-123"}).pretty()
```

### Verificar imágenes en Cloudinary
- Accede a tu dashboard de Cloudinary
- Busca en la carpeta "mascotas"
- Verifica que las imágenes se hayan subido correctamente

---

## 🔄 Automatización

### Script de setup completo
```bash
#!/bin/bash
echo "🧹 Limpiando datos..."
python cleanup_test_data.py

echo "🐾 Poblando base de datos..."
python populate_simple.py

echo "✅ Setup completado!"
echo "🌐 API disponible en: http://localhost:8000"
echo "📚 Documentación en: http://localhost:8000/docs"
```

### Script de testing
```bash
#!/bin/bash
echo "🧹 Limpiando datos de prueba..."
python cleanup_test_data.py

echo "🧪 Ejecutando pruebas..."
pytest tests/ -v

echo "🧹 Limpiando después de pruebas..."
python cleanup_test_data.py

echo "✅ Testing completado!"
```

---

## 📝 Notas Importantes

1. **Siempre limpia antes de poblar** para evitar duplicados
2. **Usa `populate_simple.py`** para desarrollo rápido
3. **Usa `populate_database.py`** solo cuando necesites imágenes
4. **Los scripts son seguros** y preguntan antes de sobrescribir datos
5. **Las imágenes se suben a Cloudinary** con IDs únicos
6. **Los datos de testing se limpian automáticamente** en las pruebas

---

## 🎯 Tokens de Prueba

Para probar la API con los datos poblados:

**Usuario (Owner)**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner
```

**Veterinaria (Clinic)**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.clinic
```

**Ejemplo de uso**:
```bash
curl -X GET "http://localhost:8000/api/v1/pets/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
``` 