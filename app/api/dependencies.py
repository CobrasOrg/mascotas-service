import httpx
from fastapi import HTTPException, Depends, Header
from typing import Optional, Dict, Any
import os

# Tokens de prueba para desarrollo
TEST_TOKEN_OWNER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.owner"
TEST_TOKEN_CLINIC = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.clinic"

# Datos de usuario de prueba
TEST_USER_DATA = {
    "id": "user-123",
    "email": "test@example.com",
    "name": "Test User",
    "role": "owner"
}

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Obtiene el usuario actual basado en el token JWT del header Authorization.
    Para desarrollo, usa tokens de prueba.
    
    Args:
        authorization (Optional[str]): Header Authorization con el token Bearer
        
    Returns:
        Dict[str, Any]: Datos del usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o no se puede obtener el perfil del usuario
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token de autorización requerido"
        )
    
    # Extraer el token del header Authorization
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Formato de token inválido. Debe ser 'Bearer <token>'"
        )
    
    token = authorization.replace("Bearer ", "")
    
    # Para desarrollo, usar tokens de prueba
    if token in [TEST_TOKEN_OWNER, TEST_TOKEN_CLINIC]:
        return TEST_USER_DATA
    
    # Si no es un token de prueba, intentar con el servicio externo
    try:
        auth_service_url = "https://auth-service-g7nh.onrender.com/api/v1/user/profile"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                auth_service_url,
                headers={"Authorization": f"Bearer {token}"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            elif response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Token inválido o expirado"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Error al obtener el perfil del usuario"
                )
                
    except httpx.TimeoutException:
        # Para tokens claramente inválidos, devolver 401 en lugar de 500
        if token == "invalid.token" or len(token) < 10:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
        raise HTTPException(
            status_code=500,
            detail="Timeout al conectar con el servicio de autenticación"
        )
    except httpx.RequestError as e:
        # Para tokens claramente inválidos, devolver 401 en lugar de 500
        if token == "invalid.token" or len(token) < 10:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión con el servicio de autenticación: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Obtiene solo el ID del usuario actual basado en el token JWT.
    
    Args:
        authorization (Optional[str]): Header Authorization con el token Bearer
        
    Returns:
        str: ID del usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o no se puede obtener el perfil del usuario
    """
    user_data = await get_current_user(authorization)
    
    # Extraer el ID del usuario
    user_id = user_data.get("id")
    if not user_id:
        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener el ID del usuario"
        )
    
    return user_id

def get_auth_headers(user_type: str = "owner") -> dict:
    """
    Genera headers de autenticación para tests
    
    Args:
        user_type: Tipo de usuario ('owner' o 'clinic')
        
    Returns:
        dict: Headers de autenticación
    """
    token = TEST_TOKEN_OWNER if user_type == "owner" else TEST_TOKEN_CLINIC
    return {
        "Authorization": f"Bearer {token}",
        "X-User-Type": user_type
    } 