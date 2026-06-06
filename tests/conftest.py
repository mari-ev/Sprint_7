import pytest
import requests
import uuid
from api_urls import ApiUrls


@pytest.fixture
def courier_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "login": f"test_courier_{unique_id}",
        "password": "password123",
        "firstName": f"Courier_{unique_id}",
    }


@pytest.fixture(scope="function")
def created_courier(courier_data):
    response = requests.post(ApiUrls.CREATE_COURIER, json=courier_data, timeout=10)
    assert response.status_code == 201
    auth_data = {
        "login": courier_data["login"],
        "password": courier_data["password"],
    }
    login_response = requests.post(ApiUrls.LOGIN_COURIER, json=auth_data, timeout=10)
    json_response = login_response.json()
    courier_id = json_response["id"]
    full_courier_info = {**courier_data, "id": courier_id}
    yield full_courier_info
    requests.delete(ApiUrls.get_delete_courier_url(courier_id), timeout=10)
