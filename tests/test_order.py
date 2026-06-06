import pytest
import allure
from test_data import (
    ORDER_WITH_BLACK,
    ORDER_WITH_GREY,
    ORDER_WITH_BOTH_COLORS,
    ORDER_WITHOUT_COLOR,
)
from methods.order_methods import OrderMethods
from methods.courier_methods import CourierMethods


@allure.feature("Работа с заказами")
class TestOrders:
    def setup_method(self):
        with allure.step("Инициализируем методы работы с заказами и курьерами"):
            self.order_methods = OrderMethods()
            self.courier_methods = CourierMethods()

    @pytest.mark.parametrize(
        "order_data,color_description",
        [
            (ORDER_WITH_BLACK, "один цвет — BLACK"),
            (ORDER_WITH_GREY, "один цвет — GREY"),
            (ORDER_WITH_BOTH_COLORS, "оба цвета"),
            (ORDER_WITHOUT_COLOR, "без цвета"),
        ],
    )
    @allure.story("Создание заказа с разными вариантами цвета")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_positive(self, order_data, color_description):
        with allure.step(f"Создаём заказ: {color_description}"):
            json_response, status_code = self.order_methods.create_order(order_data)

        with allure.step("Проверяем результат создания заказа"):
            assert (
                status_code == 201
                and "track" in json_response
                and isinstance(json_response["track"], int)
            ), f"Ошибка в сценарии '{color_description}': статус={status_code}, track_есть={'track' in json_response}, тип_track={type(json_response.get('track', None))}"

    @allure.story("Получение списка заказов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_orders_list_positive(self):
        with allure.step("Получаем список заказов"):
            list_response, list_status = self.order_methods.get_orders_list()

        with allure.step("Проверяем структуру ответа"):
            assert (
                list_status == 200
                and isinstance(list_response, dict)
                and "orders" in list_response
                and isinstance(list_response["orders"], list)
            ), f"Проверка не пройдена: статус={list_status}, тип_ответа={type(list_response).__name__}, есть_orders={'есть' if 'orders' in list_response else 'нет'}, тип_orders={type(list_response.get('orders', 'N/A')).__name__}"
