import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import json
from app.api.dependencies import get_auth_headers, TEST_TOKEN_OWNER, TEST_TOKEN_CLINIC

TEST_TOKEN_VALID = TEST_TOKEN_OWNER
TEST_TOKEN_INVALID = "invalid.token"
TEST_USER_ID = "user-123"
TEST_USER_DATA = {
    "id": TEST_USER_ID,
    "email": "test@example.com",
    "name": "Test User",
    "role": "owner"
}

class TestPetsAuthentication:
    def test_list_pets_without_token(self, client, clean_db):
        response = client.get("/api/v1/pets/")
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_list_pets_with_invalid_token(self, client, clean_db):
        headers = {"Authorization": f"Bearer {TEST_TOKEN_INVALID}"}
        response = client.get("/api/v1/pets/", headers=headers)
        assert response.status_code == 401
        assert "Token inválido" in response.json()["detail"]

    def test_list_pets_with_valid_token(self, client, clean_db):
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        response = client.get("/api/v1/pets/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_pets_by_user_id_without_token(self, client, clean_db):
        response = client.get(f"/api/v1/pets/user/{TEST_USER_ID}")
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_get_pets_by_user_id_with_valid_token(self, client, clean_db):
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        response = client.get(f"/api/v1/pets/user/{TEST_USER_ID}", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_pet_without_token(self, client, clean_db):
        pet_data = {
            "petName": "Test Pet",
            "species": "canine",
            "breed": "Beagle",
            "age": 3,
            "weight": 15.5,
            "bloodType": "DEA 1.1+",
            "lastVaccination": "2024-01-15",
            "healthStatus": "Saludable"
        }
        response = client.post("/api/v1/pets/", data=pet_data)
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_create_pet_with_valid_token(self, client, clean_db):
        pet_data = {
            "petName": "Test Pet",
            "species": "canine",
            "breed": "Beagle",
            "age": 3,
            "weight": 15.5,
            "bloodType": "DEA 1.1+",
            "lastVaccination": "2024-01-15",
            "healthStatus": "Saludable"
        }
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        response = client.post("/api/v1/pets/", data=pet_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["petName"] == "Test Pet"
        assert response.json()["ownerId"] == TEST_USER_ID

    def test_update_pet_without_token(self, client, clean_db):
        pet_id = "507f1f77bcf86cd799439011"
        pet_data = {
            "petName": "Updated Pet",
            "age": 4
        }
        response = client.put(f"/api/v1/pets/{pet_id}", data=pet_data)
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]

    def test_delete_pet_without_token(self, client, clean_db):
        pet_id = "507f1f77bcf86cd799439011"
        response = client.delete(f"/api/v1/pets/{pet_id}")
        assert response.status_code == 401
        assert "Token de autorización requerido" in response.json()["detail"]

class TestPetsAuthorization:
    def test_update_pet_not_owned(self, client, clean_db):
        from app.models.pet_mongo import PetMongoModel
        from app.schemas.pet import PetResponse
        with patch.object(PetMongoModel, 'get_pet_by_id') as mock_get_pet:
            mock_pet = PetResponse(
                id="507f1f77bcf86cd799439011",
                petName="Other User Pet",
                species="canine",
                breed="Golden Retriever",
                age=5,
                weight=25.0,
                bloodType="DEA 1.1+",
                lastVaccination="2024-01-15",
                healthStatus="Saludable",
                petPhoto=None,
                ownerId="other-user-456",
                registeredAt="2024-01-01T00:00:00",
                updatedAt="2024-01-01T00:00:00"
            )
            mock_get_pet.return_value = mock_pet
            pet_data = {
                "petName": "Updated Pet",
                "age": 4
            }
            headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
            response = client.put("/api/v1/pets/507f1f77bcf86cd799439011", data=pet_data, headers=headers)
            assert response.status_code == 403
            assert "No tienes permisos para modificar esta mascota" in response.json()["detail"]

    def test_delete_pet_not_owned(self, client, clean_db):
        from app.models.pet_mongo import PetMongoModel
        from app.schemas.pet import PetResponse
        with patch.object(PetMongoModel, 'get_pet_by_id') as mock_get_pet:
            mock_pet = PetResponse(
                id="507f1f77bcf86cd799439011",
                petName="Other User Pet",
                species="canine",
                breed="Golden Retriever",
                age=5,
                weight=25.0,
                bloodType="DEA 1.1+",
                lastVaccination="2024-01-15",
                healthStatus="Saludable",
                petPhoto=None,
                ownerId="other-user-456",
                registeredAt="2024-01-01T00:00:00",
                updatedAt="2024-01-01T00:00:00"
            )
            mock_get_pet.return_value = mock_pet
            headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
            response = client.delete("/api/v1/pets/507f1f77bcf86cd799439011", headers=headers)
            assert response.status_code == 403
            assert "No tienes permisos para eliminar esta mascota" in response.json()["detail"]

class TestPetsUserAssociation:
    def test_create_pet_associates_with_user(self, client, clean_db):
        pet_data = {
            "petName": "Test Pet",
            "species": "canine",
            "breed": "Beagle",
            "age": 3,
            "weight": 15.5,
            "bloodType": "DEA 1.1+",
            "lastVaccination": "2024-01-15",
            "healthStatus": "Saludable"
        }
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        response = client.post("/api/v1/pets/", data=pet_data, headers=headers)
        assert response.status_code == 201
        assert response.json()["ownerId"] == TEST_USER_ID

    def test_list_pets_returns_only_user_pets(self, client, clean_db):
        pet_data_1 = {
            "petName": "User Pet 1",
            "species": "canine",
            "breed": "Beagle",
            "age": 3,
            "weight": 15.5,
            "bloodType": "DEA 1.1+",
            "lastVaccination": "2024-01-15",
            "healthStatus": "Saludable"
        }
        pet_data_2 = {
            "petName": "User Pet 2",
            "species": "feline",
            "breed": "Siamés",
            "age": 2,
            "weight": 4.5,
            "bloodType": "A",
            "lastVaccination": "2024-02-20",
            "healthStatus": "Saludable"
        }
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        response1 = client.post("/api/v1/pets/", data=pet_data_1, headers=headers)
        response2 = client.post("/api/v1/pets/", data=pet_data_2, headers=headers)
        assert response1.status_code == 201
        assert response2.status_code == 201
        response = client.get("/api/v1/pets/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert any(pet["petName"] == "User Pet 1" for pet in data)
        assert any(pet["petName"] == "User Pet 2" for pet in data)

    def test_get_pets_by_user_id_returns_correct_pets(self, client, clean_db):
        pet_data = {
            "petName": "Test Pet",
            "species": "canine",
            "breed": "Beagle",
            "age": 3,
            "weight": 15.5,
            "bloodType": "DEA 1.1+",
            "lastVaccination": "2024-01-15",
            "healthStatus": "Saludable"
        }
        headers = {"Authorization": f"Bearer {TEST_TOKEN_VALID}"}
        create_response = client.post("/api/v1/pets/", data=pet_data, headers=headers)
        assert create_response.status_code == 201
        response = client.get(f"/api/v1/pets/user/{TEST_USER_ID}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert any(pet["petName"] == "Test Pet" for pet in data) 