import requests
import random
import json
import config
from config import IOKA_PAY_CONFIGS


class PayLinkIoka2:
    api_key = IOKA_PAY_CONFIGS.get('IOKA_API_KEY')
    test_server_url = "https://stage-api.ioka.kz/v2/orders"
    url = "https://stage-api.ioka.kz/v2/orders"
    # url = "https://api.ioka.kz/v2/orders"
    back_url = "https://t.me/pdd_good_bot/"
    success_url = "https://www.google.com"
    failure_url = "https://www.yandex.ru"

    def __init__(self, telegram_id: int, price: int, currency: str, name: str, tariff: str):
        self.telegram_id = telegram_id
        self.price = price
        self.currency = currency
        self.name = name
        self.tariff = tariff

    def get_headers(self) -> dict:
        """формируем заголовок запроса"""
        headers = {"Content-Type": "application/json; charset=utf-8", "API-KEY": self.api_key}
        return headers

    def get_json_data(self, order_id) -> dict:
        """
        основное тело запроса на сервер IOKA
        """
        json_data = {
            "amount": self.price,                                   # обязательный
            "currency": self.currency,
            "capture_method": "AUTO",
            "external_id": order_id,
            "back_url": self.back_url,
            "extra_info": {"name": self.name, "client_id": str(self.telegram_id), "tariff": self.tariff},
            "success_url": self.success_url,
            "failure_url": self.failure_url,
            "template": "3D"
        }
        return json_data

    def get_pay_url(self) -> str:
        """
        сделать POST запрос в сервис Ioka и получить персональную платежную ссылку с метаданными пользователя
        order_id от 1 до 2 147 483 647
        :return: платежная ссылка
        """
        headers = self.get_headers()
        while True:
            order_id = random.choice(range(1, 2147483647))
            json_data = self.get_json_data(order_id)
            response = requests.post(self.test_server_url, headers=headers, json=json_data)
            print(response.json())
            if response.ok:
                url = response.json()["url"]
                return url


pay_link = PayLinkIoka2(telegram_id=config.ADMIN_ID, price=50000, currency="KZT", name="TESTER",
                        tariff="TEST_PREMIUM")
