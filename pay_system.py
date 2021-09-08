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

# @dp.message_handler(commands=["pay"])
# async def command_pay(message: types.Message):
#     """
#     Раздел Оплаты. Отдает ссылку на оплату доступа к образовательной системе.
#     user.country поменял на KZ, ибо доступен прием платежей только в тенге, сорян...
#     """
#     telegram_id = message.from_user.id
#     user = get_user_by(telegram_id)
#     user_country = 'KZ'
#     user_language = user.language
#     monetary_unit = get_monetary_unit(user_country, user_language)
#     price = get_finally_price_by(user.price_in_rubles, user_country)
#     pay_message_text = MESSAGE[f'pay_message_{user_language}'] + f' {str(price)} {monetary_unit}!'
#     pay_link = PayLink(login=config.PAY_CONFIGS[f'KASSA_24_LOGIN_{user_language}'],
#                        password=config.PAY_CONFIGS[f'KASSA_24_PASSWORD_{user_language}'],
#                        telegram_id=telegram_id, price_in_tenge=price)
#     url = pay_link.get_pay_url()
#
#     markup = types.InlineKeyboardMarkup()
#     pay_button = BUTTONS[f'pay_{user_language}']
#     pay_link = types.InlineKeyboardButton(text=pay_button, url=url)
#     markup.add(pay_link)
#
#     await message.answer(pay_message_text, reply_markup=markup)
