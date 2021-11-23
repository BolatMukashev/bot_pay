from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import pay_button_call
from messages import BUTTONS


def get_pay_keyboard(language: str) -> InlineKeyboardMarkup:
    pay_keyboard = InlineKeyboardMarkup()
    pay_button_1 = InlineKeyboardButton(text=BUTTONS[f'pay_premium_{language}'],
                                        callback_data=pay_button_call.new(pay_button='pay_button', value='premium'))
    pay_button_2 = InlineKeyboardButton(text=BUTTONS[f'pay_premium_max_{language}'],
                                        callback_data=pay_button_call.new(pay_button='pay_button', value='premium_max'))
    pay_keyboard.add(pay_button_1)
    pay_keyboard.add(pay_button_2)
    return pay_keyboard
