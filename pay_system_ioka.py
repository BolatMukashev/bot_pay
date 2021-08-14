import requests
import random


class PayLinkIoka:
    secret_key = "DQPzyf2HK02U9rcID2vGCzFVVcmmMcvPcrw7ELe-zx_O9bQKJ_zZKw_uPLhGEMnFOxY-zhOggvg8NUv3ZAevNQ"
    url = "https://stage.ioka.kz/api/payments/register/"
    back_url = "https://t.me/pdd_good_bot/"
    callback_url = "https://pddgoodbot.ru/accept"

    def __init__(self, telegram_id: int, price_in_tenge: int, currency: int):
        self.telegram_id = telegram_id
        self.price_in_tenge = price_in_tenge
        self.currency = currency

    def get_headers(self) -> dict:
        """формируем заголовок запроса"""
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "bearer " + self.secret_key}
        return headers

    def get_json_data(self, order_id) -> dict:
        """
        основное тело запроса
        (398 - код тенге, 643 - код рубля)
        """
        json_data = {
            "order_id": order_id,
            "currency": self.currency,
            "amount": str(self.price_in_tenge),
            "client_id": str(self.telegram_id),
            "back_url": self.back_url,
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


# new_payment = PayLinkIoka(111222555, 500)
# print(new_payment.get_pay_url())
