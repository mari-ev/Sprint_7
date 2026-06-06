import requests
import json
from api_urls import ApiUrls


class OrderMethods:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def create_order(self, order_data=None):
        """Создаёт заказ, возвращает (json_response, status_code)."""
        if order_data is None:
            order_data = {}
        response = requests.post(ApiUrls.ORDERS, json=order_data, headers=self.headers)
        try:
            return response.json(), response.status_code
        except json.decoder.JSONDecodeError:
            return response.text, response.status_code

    def get_orders_list(self):
        """Получает список заказов, возвращает (json_response, status_code)."""
        response = requests.get(ApiUrls.ORDERS, headers=self.headers)
        try:
            return response.json(), response.status_code
        except json.decoder.JSONDecodeError:
            return response.text, response.status_code

    def accept_order(self, courier_id, order_id):
        """Принимает заказ, возвращает (json_response, status_code)."""
        accept_data = {"courier_id": courier_id, "order_id": order_id}
        response = requests.post(
            ApiUrls.ACEPT_ORDER, json=accept_data, headers=self.headers
        )
        try:
            return response.json(), response.status_code
        except json.decoder.JSONDecodeError:
            return response.text, response.status_code

    def get_order_by_number(self, track_number):
        """Получает заказ по номеру, возвращает (json_response, status_code)."""
        url = ApiUrls.get_order_by_number_url(track_number)
        response = requests.get(url, headers=self.headers)
        try:
            return response.json(), response.status_code
        except json.decoder.JSONDecodeError:
            return response.text, response.status_code
