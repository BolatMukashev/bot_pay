from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from messages import BUTTONS


def get_cancel_button(language: str):
    cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = KeyboardButton(text=BUTTONS[f'cancel_{language}'])
    cancel_keyboard.add(cancel_button)
    return cancel_keyboard
