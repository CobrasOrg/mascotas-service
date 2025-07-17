# Guía de Autorización en Swagger

## 🔐 Cómo autorizarse en Swagger UI

### 1. Acceder a Swagger UI
- Ve a: `http://localhost:8000/docs`
- Verás la interfaz de Swagger con todos los endpoints disponibles

### 2. Autorizarse
1. **Haz clic en el botón "Authorize"** (🔒) en la parte superior derecha
2. **En el campo "Value" ingresa tu token JWT:**
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner
   ```
3. **Haz clic en "Authorize"**
4. **Cierra el modal**

### 3. Tokens de Prueba Disponibles

#### Para Usuarios (Owners):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner
```

#### Para Veterinarias (Clinics):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.clinic
```

### 4. Probar Endpoints

Una vez autorizado, puedes probar cualquier endpoint:

#### GET /api/v1/pets/
- **Descripción**: Obtiene todas las mascotas del usuario autenticado
- **Autorización**: Requerida
- **Respuesta**: Lista de mascotas del usuario

#### POST /api/v1/pets/
- **Descripción**: Crea una nueva mascota
- **Autorización**: Requerida
- **Formato**: multipart/form-data
- **Campos requeridos**:
  - `petName`: Nombre de la mascota
  - `species`: Especie (canine, feline, etc.)
  - `breed`: Raza
  - `age`: Edad en años
  - `weight`: Peso en kg
  - `bloodType`: Tipo de sangre
  - `lastVaccination`: Fecha de vacunación (YYYY-MM-DD)
  - `healthStatus`: Estado de salud
  - `petPhoto`: Foto (opcional)

#### PUT /api/v1/pets/{pet_id}
- **Descripción**: Actualiza una mascota existente
- **Autorización**: Requerida
- **Nota**: Solo puedes actualizar tus propias mascotas

#### DELETE /api/v1/pets/{pet_id}
- **Descripción**: Elimina una mascota
- **Autorización**: Requerida
- **Nota**: Solo puedes eliminar tus propias mascotas

### 5. Ejemplos de Uso

#### Crear una mascota:
```bash
curl -X POST "http://localhost:8000/api/v1/pets/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner" \
  -F "petName=Luna" \
  -F "species=feline" \
  -F "breed=Siamés" \
  -F "age=3" \
  -F "weight=4.5" \
  -F "bloodType=A" \
  -F "lastVaccination=2024-01-15" \
  -F "healthStatus=Saludable"
```

#### Obtener mascotas del usuario:
```bash
curl -X GET "http://localhost:8000/api/v1/pets/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
```

### 6. Códigos de Respuesta

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **204**: Recurso eliminado exitosamente
- **302**: Redirección (para fotos)
- **400**: Error en la solicitud
- **401**: No autorizado (token requerido o inválido)
- **403**: Prohibido (no tienes permisos)
- **404**: Recurso no encontrado
- **422**: Error de validación
- **500**: Error interno del servidor

### 7. Características de Seguridad

- ✅ **Autenticación JWT**: Todos los endpoints principales requieren token
- ✅ **Autorización**: Los usuarios solo pueden acceder a sus propias mascotas
- ✅ **Validación**: Todos los datos se validan antes de procesarse
- ✅ **Seguridad**: Tokens de prueba para desarrollo

### 8. Troubleshooting

#### Error 401 - No autorizado:
- Verifica que hayas ingresado el token correctamente
- Asegúrate de incluir "Bearer " antes del token
- Usa uno de los tokens de prueba proporcionados

#### Error 403 - Prohibido:
- Solo puedes modificar/eliminar tus propias mascotas
- Verifica que el ID de la mascota sea correcto

#### Error 422 - Validación:
- Verifica que todos los campos requeridos estén presentes
- Asegúrate de que los valores sean del tipo correcto
- Revisa que las especies y razas sean válidas

### 9. Desarrollo vs Producción

#### Desarrollo:
- Usa los tokens de prueba proporcionados
- No necesitas un servicio de autenticación externo
- Los tokens simulan usuarios reales

#### Producción:
- Implementa un servicio de autenticación real
- Genera tokens JWT válidos
- Configura el servicio de autenticación externo

### 10. Notas Importantes

- **El endpoint `/photo/{pet_id}` no requiere autorización** para facilitar el acceso a las imágenes
- **Los tokens de prueba son para desarrollo únicamente**
- **En producción, implementa un sistema de autenticación real**
- **Los usuarios solo pueden ver y modificar sus propias mascotas** 