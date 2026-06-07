import pytest
import requests
import allure
from methods.courier_methods import CourierMethods
from helpers import generate_courier_data, register_courier_for_cleanup


@allure.feature("Работа с курьерами")
@allure.description(
    "Тесты для проверки основных операций с курьерами: создание, авторизация, удаление и обработка ошибок"
)
class TestCourier:

    @allure.story("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: создание курьера с корректными данными")
    def test_create_courier_success(self, courier_cleanup):
        with allure.step("Подготавливаем данные курьера"):
            courier_data = generate_courier_data()
            courier_methods = CourierMethods()

            register_courier_for_cleanup(courier_data, courier_cleanup)

        with allure.step("Отправляем запрос на создание курьера"):
            json_response, status_code = courier_methods.create_courier(courier_data)

        with allure.step("Проверяем успешный статус 201 и наличие флага 'ok'"):
            assert (
                status_code == 201
                and "ok" in json_response
                and json_response["ok"] is True
            ), f"status_code: {status_code}, response: {json_response}"

    @allure.story("Успешная авторизация курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: авторизация существующего курьера")
    def test_login_success(self, created_courier):
        with allure.step("Формируем данные для авторизации"):
            courier_methods = CourierMethods()
            auth_data = {
                "login": created_courier["original_data"]["login"],
                "password": created_courier["original_data"]["password"],
            }

        with allure.step("Выполняем запрос авторизации"):
            json_response, status_code, courier_id = courier_methods.login_courier(auth_data)


        with allure.step("Проверяем статус 200 и наличие поля 'id' в ответе"):
            assert (
                status_code == 200 and "id" in json_response
            ), f"status_code: {status_code}, response: {json_response}"

    @allure.story("Успешное удаление курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: удаление существующего курьера")
    def test_delete_courier_success(self, created_courier):
        with allure.step("Получаем ID курьера для удаления"):
            courier_id = created_courier["id"]

        with allure.step("Инициализируем методы работы с курьерами"):
            courier_methods = CourierMethods()

        with allure.step("Выполняем запрос на удаление курьера"):
            json_response, status_code = courier_methods.delete_courier(courier_id)

        with allure.step("Проверяем статус 200 и наличие флага 'ok'"):
            assert (
                status_code == 200
                and "ok" in json_response
                and json_response["ok"] is True
            ), f"status_code: {status_code}, response: {json_response}"

    @allure.story("Обработка дублирования при создании курьера")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест: попытка создать курьера с уже существующим логином")
    def test_create_duplicate_courier(self, courier_cleanup):
        with allure.step("Создаём курьера первый раз (успешно)"):
            courier_data = generate_courier_data()
            courier_methods = CourierMethods()
            json_response, status_code = courier_methods.create_courier(courier_data)
            register_courier_for_cleanup(courier_data, courier_cleanup)


        with allure.step("Пытаемся создать курьера с тем же логином"):
            json_response, status_code = courier_methods.create_courier(courier_data)

        with allure.step("Проверяем статус 409 и сообщение об ошибке"):
            assert (
                status_code == 409
                and "message" in json_response
                and "Этот логин уже используется" in json_response["message"]
            ), f"status_code: {status_code}, response: {json_response}"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.story("Обработка отсутствующих полей при создании курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: создание курьера без обязательных полей")
    def test_create_courier_missing_fields(self, courier_cleanup, missing_field):
        with allure.step("Подготавливаем данные курьера"):
            courier_data = generate_courier_data()
            register_courier_for_cleanup(courier_data, courier_cleanup)

        with allure.step(f"Удаляем обязательное поле '{missing_field}' из данных"):
            incomplete_data = courier_data.copy()
            del incomplete_data[missing_field]

        with allure.step("Отправляем запрос с неполными данными"):
            courier_methods = CourierMethods()
            json_response, status_code = courier_methods.create_courier(incomplete_data)

        with allure.step("Проверяем статус 400 и сообщение об ошибке"):
            assert (
                status_code == 400
                and "message" in json_response
                and "Недостаточно данных для создания учетной записи"
                in json_response["message"]
            ), f"status_code: {status_code}, response: {json_response}"

    @pytest.mark.parametrize(
        "wrong_field,wrong_value",
        [("login", "wrong_login"), ("password", "wrong_password")],
    )
    @allure.story("Обработка неверных учётных данных при авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: авторизация с неверными учётными данными")
    def test_login_wrong_credentials(self, courier_cleanup, wrong_field, wrong_value):
        with allure.step("Подготавливаем данные курьера"):
            courier_data = generate_courier_data()
            register_courier_for_cleanup(courier_data, courier_cleanup)
            
        with allure.step(f"Подменяем поле '{wrong_field}' на некорректное значение"):
            wrong_data = courier_data.copy()
            wrong_data[wrong_field] = wrong_value

        with allure.step("Выполняем запрос авторизации с неверными данными"):
            courier_methods = CourierMethods()
            json_response, status_code, _ = courier_methods.login_courier(wrong_data)

        with allure.step("Проверяем статус 404 и сообщение об ошибке"):
            assert (
                status_code == 404
                and "message" in json_response
                and "Учетная запись не найдена" in json_response["message"]
            ), f"status_code: {status_code}, response: {json_response}"

    @allure.story("Обработка отсутствия логина при авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Тест: авторизация без указания логина")
    def test_login_missing_login(self, created_courier):
        with allure.step("Формируем данные авторизации из original_data"):
            auth_data = {
                "login": created_courier["original_data"]["login"],
                "password": created_courier["original_data"]["password"]}

        with allure.step("Удаляем поле 'login' из данных авторизации"):
            del auth_data["login"]

        with allure.step("Выполняем запрос авторизации без логина"):
            courier_methods = CourierMethods()
            json_response, status_code, _ = courier_methods.login_courier(auth_data)

        with allure.step("Проверяем статус 400 и сообщение об ошибке"):
            assert (
                status_code == 400
                and "Недостаточно данных для входа" in json_response.get("message", "")
            ), f"status_code: {status_code}, response: {json_response}"

    @allure.story("Обработка отсутствия пароля при авторизации")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Тест: авторизация без указания пароля (ожидается таймаут)")
    @allure.description(
        "Проверяет, что API возвращает таймаут при отправке запроса на авторизацию "
        "без поля 'password'. Соответствует реальному поведению API, "
        "хотя в документации ожидается статус 400."
    )
    def test_login_missing_password(self, created_courier):
        with allure.step("Формируем данные авторизации из original_data"):
            auth_data = {
                "login": created_courier["original_data"]["login"],
                "password": created_courier["original_data"]["password"]
                }
            
        with allure.step("Подготавливаем данные: удаляем поле 'password'"):
            del auth_data["password"]

        with allure.step("Инициализируем методы работы с курьерами"):
            courier_methods = CourierMethods()

        with allure.step("Выполняем запрос авторизации без пароля и ожидаем таймаут"):
            with pytest.raises(requests.exceptions.ReadTimeout):
                courier_methods.login_courier(auth_data)

    @allure.story("Обработка удаления курьера с несуществующим ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Тест: попытка удалить курьера с несуществующим ID")
    def test_delete_courier_invalid_id(self):
        with allure.step("Задаём заведомо несуществующий ID курьера"):
            invalid_id = 999999

        with allure.step("Инициализируем методы работы с курьерами"):
            courier_methods = CourierMethods()

        with allure.step("Выполняем запрос на удаление курьера с несуществующим ID"):
            json_response, status_code = courier_methods.delete_courier(invalid_id)

        with allure.step("Проверяем статус 404 и сообщение об ошибке"):
            assert (
                status_code == 404
                and "message" in json_response
                and "Курьера с таким id нет" in json_response["message"]
            ), f"status_code: {status_code}, response: {json_response}"
