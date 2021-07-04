import requests
import base64


class PayLink:
    kassa24_url = 'https://ecommerce.pult24.kz/payment/create'
    site_to_return = "https://t.me/pdd_good_bot"
    site_to_send_callback = "https://pddgoodbot.ru/accept_page"
    description = "Покупка годового доступа к образовательной платформе PDDgoodbot на базе мессенджера Telegram"
    # email = "pdd.good.bot@gmail.com"
    # phone = "7085292078"

    def __init__(self, login: str, password: str, telegram_id, price_in_tenge: int):
        self.login = login
        self.password = password
        self.telegram_id = telegram_id
        self.price_in_tenge = price_in_tenge
        self.login_and_password = self.login + ':' + self.password

    def encode_to_base64(self) -> str:
        """формируем Basic access authentication для заголовка"""
        sample_string_bytes = self.login_and_password.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def get_headers(self) -> dict:
        """формируем заголовок запроса"""
        base64_string = self.encode_to_base64()
        headers = {"Content-Type": "application/json", "Authorization": "Basic " + base64_string}
        return headers

    def get_json_data(self) -> dict:
        """основное тело запроса"""
        json_data = {
            "merchantId": self.login,
            "amount": self.price_in_tenge * 100,
            "returnUrl": self.site_to_return,
            "callbackUrl": self.site_to_send_callback,
            "description": self.description,
            "customerData": {},
            "metadata": {
                "telegram_id": self.telegram_id
            }
        }
        return json_data

    def get_pay_url(self) -> str:
        """сделать POST запрос в сервис Kassa24 и получить персональную платежную ссылку с метаданными пользователя"""
        headers = self.get_headers()
        json_data = self.get_json_data()
        response = requests.post(self.kassa24_url, headers=headers, json=json_data)
        if response.ok:
            url = response.json()['url']
            return url
