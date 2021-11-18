from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_url_button(text: str, url: str) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с одной кнопкой, с приклепленной к ней ссылкой
    :param text: Текст на кнопке
    :param url: Ссылка
    :return: Клавиатура с кнопкой
    """
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text=text, url=url)
    keyboard.add(button)
    return keyboard
