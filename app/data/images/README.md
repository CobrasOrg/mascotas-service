# Imágenes de Prueba

Este directorio contiene imágenes de prueba para los tests del servicio de mascotas.

## Archivos Requeridos

Para que los tests funcionen correctamente, agrega las siguientes imágenes:

- `perro.jpg` - Imagen de un perro para tests
- `gato.jpg` - Imagen de un gato para tests

## Formato

- **Formato**: JPEG (.jpg)
- **Tamaño**: Recomendado máximo 1MB
- **Resolución**: Mínimo 100x100 píxeles

## Uso

Los tests automáticamente usarán estas imágenes cuando estén disponibles.
Si no se encuentran, usarán imágenes sintéticas como fallback.

## Ejemplo

```python
# En los tests
image_data, filename = get_image_bytes_for_species("canine")
files = {"petPhoto": (filename, image_data, "image/jpeg")}
``` 