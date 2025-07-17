#!/usr/bin/env python3
"""
Test Rápido para Desarrollo Local
Ejecuta solo los tests más críticos para validación rápida
"""

import sys
import os
import subprocess
import asyncio
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🧪 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        return False

def run_pytest_specific(test_path, description):
    """Ejecuta un test específico con pytest"""
    command = f"python -m pytest {test_path} -v --tb=short"
    return run_command(command, description)

async def main():
    """Función principal del test rápido"""
    print("🚀 Iniciando Test Rápido para Desarrollo Local")
    print("=" * 50)
    
    # Lista de tests críticos para validación rápida
    critical_tests = [
        # Tests de funcionalidad básica (críticos)
        ("tests/test_pets.py::test_create_pet_without_photo", "Test creación de mascota"),
        ("tests/test_pets.py::test_get_pets_by_owner", "Test obtener mascotas del usuario"),
        ("tests/test_pets.py::test_update_pet", "Test actualizar mascota"),
        ("tests/test_pets.py::test_delete_pet", "Test eliminar mascota"),
        # Tests de autenticación (críticos)
        ("tests/test_pets_authentication.py::test_get_pets_with_auth", "Test autenticación"),
        ("tests/test_pets_authentication.py::test_create_pet_with_auth", "Test crear con auth"),
    ]
    
    success_count = 0
    total_tests = len(critical_tests)
    
    for test_path, description in critical_tests:
        if run_pytest_specific(test_path, description):
            success_count += 1
        print()
    
    # Resumen final
    print("=" * 50)
    print(f"📊 Resumen: {success_count}/{total_tests} tests pasaron")
    
    if success_count == total_tests:
        print("✅ Todos los tests críticos pasaron")
        print("💡 Puedes proceder con el desarrollo")
        return 0
    else:
        print("❌ Algunos tests críticos fallaron")
        print("🔧 Revisa los errores antes de continuar")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 