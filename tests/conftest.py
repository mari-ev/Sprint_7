import pytest
from helpers import create_and_authorize_courier, delete_courier_by_id
from methods.courier_methods import CourierMethods

@pytest.fixture(scope="function")
def created_courier():
    full_courier_info = create_and_authorize_courier()
    yield full_courier_info
    delete_courier_by_id(full_courier_info["id"])

@pytest.fixture
def courier_cleanup(request):
    couriers_to_delete = []

    def register_for_cleanup(credentials):
        couriers_to_delete.append(credentials)

    def _perform_cleanup():
        for credentials in couriers_to_delete:
            courier_methods = CourierMethods()
            _, _, courier_id = courier_methods.login_courier(credentials)
            delete_courier_by_id(courier_id)

    request.addfinalizer(_perform_cleanup)
    return register_for_cleanup
