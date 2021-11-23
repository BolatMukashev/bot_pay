import requests
import random
from config import IOKA_PAY_CONFIGS


class PayLinkIoka:
    secret_key = IOKA_PAY_CONFIGS.get('IOKA_SECRET_KEY')
    test_server_url = "https://stage.ioka.kz/api/payments/register/"
    url = "https://ioka.kz/api/payments/register/"
    back_url = "https://t.me/pdd_good_bot/"
    callback_url = "https://pddgoodbot.ru/accept"

    def __init__(self, telegram_id: int, price: int, currency: int, name: str, tariff: str):
        self.telegram_id = telegram_id
        self.price = price
        self.currency = currency
        self.name = name
        self.tariff = tariff

    def get_headers(self) -> dict:
        """формируем заголовок запроса"""
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + self.secret_key}
        return headers

    def get_json_data(self, order_id) -> dict:
        """
        основное тело запроса на сервер IOKA
        """
        json_data = {
            "amount": str(self.price),                          # обязательный
            "currency": self.currency,
            "order_id": order_id,                               # обязательный
            "back_url": self.back_url,                          # обязательный
            "additional_params": {"name": self.name,
                                  "tariff": self.tariff},
            "client_id": str(self.telegram_id),
            "callback_url": self.callback_url,
            "template": "3D"
        }
        return json_data

    def get_pay_url(self) -> str:
        """сделать POST запрос в сервис Ioka и получить персональную платежную ссылку с метаданными пользователя"""
        headers = self.get_headers()
        while True:
            # order_id до 2147483647
            order_id = random.choice(range(0, 2147483647))
            json_data = self.get_json_data(order_id)
            response = requests.post(self.url, headers=headers, json=json_data)
            if response.ok:
                url = response.json()["url"]
                return url
