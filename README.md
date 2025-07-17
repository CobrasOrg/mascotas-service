# API de Mascotas Service

API para gestión de mascotas con soporte para imágenes, MongoDB y autenticación JWT.

## Características

- FastAPI como framework web
- MongoDB como base de datos
- Autenticación JWT mediante servicio externo
- Gestión de mascotas asociadas a usuarios
- Soporte para imágenes con Cloudinary
- Estructura modular y escalable
- Configuración de CORS
- Variables de entorno con python-dotenv
- Husky para validación de mensajes de commit
- Pre-commit hooks para linting y formateo

## Requisitos

- Python 3.8+
- MongoDB
- Node.js y npm (para Husky)
- pip

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/mascotas-service.git
cd mascotas-service
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias de Python:

```bash
pip install -r requirements.txt
```

4. Instalar dependencias de Node.js:

```bash
npm install
```

5. Configurar variables de entorno:

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## Configuración de Variables de Entorno

Crear un archivo `.env` con las siguientes variables:

```env
# MongoDB
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/mascotas?retryWrites=true&w=majority
MONGODB_DATABASE=mascotas

# MongoDB Testing
MONGODB_TEST_URL=mongodb+srv://username:password@cluster.mongodb.net/mascotas_test?retryWrites=true&w=majority
MONGODB_TEST_DATABASE=mascotas_test

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# Application
APP_ENV=development
DEBUG=true
```

## Ejecución

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en:

- http://localhost:8000 - Mensaje de bienvenida
- http://localhost:8000/api/v1/base/health - Health check
- http://localhost:8000/docs - Documentación Swagger UI
- http://localhost:8000/redoc - Documentación ReDoc

## Autenticación

La API utiliza autenticación JWT mediante un servicio externo. Para usar los endpoints protegidos:

1. Obtener un token JWT del servicio de autenticación
2. Incluir el token en el header `Authorization: Bearer <token>`

### Servicio de Autenticación

- **URL**: https://auth-service-g7nh.onrender.com/api/v1/user/profile
- **Método**: GET
- **Headers**: `Authorization: Bearer <token>`

## Endpoints de Mascotas

### Obtener mascotas del usuario autenticado
```http
GET /api/v1/pets/
Authorization: Bearer <token>
```

### Obtener mascotas por ID de usuario específico
```http
GET /api/v1/pets/user/{user_id}
Authorization: Bearer <token>
```

### Crear nueva mascota
```http
POST /api/v1/pets/
Authorization: Bearer <token>
Content-Type: multipart/form-data

petName: "Luna"
species: "feline"
breed: "Siamés"
age: 3
weight: 4.5
bloodType: "A"
lastVaccination: "2024-01-15"
healthStatus: "Saludable"
petPhoto: [archivo opcional]
```

### Actualizar mascota
```http
PUT /api/v1/pets/{pet_id}
Authorization: Bearer <token>
Content-Type: multipart/form-data

petName: "Luna Actualizada"
age: 4
petPhoto: [archivo opcional]
```

### Eliminar mascota
```http
DELETE /api/v1/pets/{pet_id}
Authorization: Bearer <token>
```

### Obtener foto de mascota
```http
GET /api/v1/pets/photo/{pet_id}
```

## Características de Seguridad

### Asociación de Usuarios
- Todas las mascotas se asocian automáticamente al usuario que las crea
- Los usuarios solo pueden ver, modificar y eliminar sus propias mascotas
- El endpoint `/user/{user_id}` permite consultar mascotas de usuarios específicos

### Autorización
- Todos los endpoints principales requieren autenticación JWT
- Verificación de propiedad antes de modificar/eliminar mascotas
- Códigos de respuesta apropiados (401, 403, 404)

### Validación de Datos
- Validación de esquemas con Pydantic
- Validación de razas por especie
- Validación de tipos de sangre
- Validación de rangos de edad y peso

## Estructura del Proyecto

```
mascotas-service/
├── app/
│   ├── api/
│   │   ├── dependencies.py          # Dependencias de autenticación
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── base.py
│   │       │   └── pets.py          # Endpoints de mascotas
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── enums.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── base.py
│   │   └── pet_mongo.py
│   ├── schemas/
│   │   ├── base.py
│   │   └── pet.py
│   └── services/
│       ├── cloudinary_service.py
│       └── pet_service.py
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_pets.py
│   └── test_pets_authentication.py  # Pruebas de autenticación
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── commitlint.config.js
├── main.py
├── package.json
├── pytest.ini
├── README.md
└── requirements.txt
```

## Testing

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar pruebas específicas
```bash
pytest tests/test_pets_authentication.py -v
pytest tests/test_pets.py -v
```

### Ejecutar pruebas con coverage
```bash
pytest --cov=app tests/
```

## Desarrollo

### Pre-commit hooks
Los hooks se ejecutan automáticamente antes de cada commit:

```bash
pre-commit install
```

### Linting y formateo
```bash
# Formatear código
black app/ tests/

# Linting
flake8 app/ tests/
```

### Validación de commits
```bash
# Ejemplo de commit válido
git commit -m "feat: agregar autenticación JWT a endpoints de mascotas"

# Ejemplo de commit inválido
git commit -m "agregar cosas"  # ❌ No cumple con conventional commits
```

## Despliegue

### Variables de entorno para producción
```env
APP_ENV=production
DEBUG=false
MONGODB_URL=tu_url_de_produccion
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

### Docker (opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
