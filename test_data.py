BASE_ORDER_DATA = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
}

ORDER_WITH_BLACK = BASE_ORDER_DATA.copy()
ORDER_WITH_BLACK["color"] = ["BLACK"]

ORDER_WITH_GREY = BASE_ORDER_DATA.copy()
ORDER_WITH_GREY["color"] = ["GREY"]


ORDER_WITH_BOTH_COLORS = BASE_ORDER_DATA.copy()
ORDER_WITH_BOTH_COLORS["color"] = ["BLACK", "GREY"]


ORDER_WITHOUT_COLOR = BASE_ORDER_DATA.copy()
