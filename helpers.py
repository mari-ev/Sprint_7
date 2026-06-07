import uuid
from methods.courier_methods import CourierMethods

def generate_courier_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "login": f"test_courier_{unique_id}",
        "password": "password123",
        "firstName": f"Courier_{unique_id}",
    }

def create_and_authorize_courier():
    courier_methods = CourierMethods()
    courier_data = generate_courier_data()

    create_response, create_status = courier_methods.create_courier(courier_data)

    auth_data = {
        "login": courier_data["login"],
        "password": courier_data["password"],
    }
    login_response, login_status, courier_id = courier_methods.login_courier(auth_data)

    return {
        "original_data": courier_data,
        "create_response": create_response,
        "create_status": create_status,
        "login_response": login_response,
        "login_status": login_status,
        "id": courier_id
    }

def delete_courier_by_id(courier_id):
    courier_methods = CourierMethods()
    json_response, status_code = courier_methods.delete_courier(courier_id)
    return {
        "response": json_response,
        "status_code": status_code
    }

def register_courier_for_cleanup(courier_data, courier_cleanup):
    """Регистрирует курьера для автоматической очистки после теста."""
    courier_cleanup({
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
