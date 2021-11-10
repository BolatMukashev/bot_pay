from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from messages import BUTTONS


def get_pay_button(language: str, url: str):
    pay_keyboard = InlineKeyboardMarkup()
    pay_button = InlineKeyboardButton(text=BUTTONS[f'pay_{language}'], url=url)
    pay_keyboard.add(pay_button)
    return pay_keyboard
