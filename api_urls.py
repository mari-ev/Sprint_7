class ApiUrls:
    """Класс для хранения URL API."""

    BASE_URL = "https://qa-scooter.education-services.ru/api/v1"
    CREATE_COURIER = f"{BASE_URL}/courier"
    ORDERS = f"{BASE_URL}/orders"
    LOGIN_COURIER = f"{BASE_URL}/courier/login"
    DELETE_COURIER = f"{BASE_URL}/courier/"

    @classmethod
    def get_delete_courier_url(cls, courier_id=None):
        """Возвращает URL для удаления курьера.
        Если courier_id не указан, возвращает базовый URL без ID.
        """
        if courier_id is None:
            return cls.DELETE_COURIER
        else:
            return f"{cls.DELETE_COURIER}{courier_id}"
