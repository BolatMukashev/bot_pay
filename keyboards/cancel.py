from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages import BUTTONS


def get_cancel_button(language: str):
    cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = KeyboardButton(text=BUTTONS[f'cancel_{language}'])
    cancel_markup.add(cancel_button)
    return cancel_markup
