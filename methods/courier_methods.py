import requests
from api_urls import ApiUrls


class CourierMethods:
    def __init__(self, timeout=10):
        self.headers = {"Content-Type": "application/json"}
        self.timeout = timeout

    def create_courier(self, courier_data):
        response = requests.post(
            ApiUrls.CREATE_COURIER,
            json=courier_data,
            headers=self.headers,
            timeout=self.timeout,
        )
        return response.json(), response.status_code

    def login_courier(self, login_data):
        response = requests.post(
            ApiUrls.LOGIN_COURIER,
            json=login_data,
            headers=self.headers,
            timeout=self.timeout,
        )
        json_response = response.json()
        courier_id = json_response.get("id")
        return json_response, response.status_code, courier_id

    def delete_courier(self, courier_id):
        url = ApiUrls.get_delete_courier_url(courier_id)
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return response.json(), response.status_code
