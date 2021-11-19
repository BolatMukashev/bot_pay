from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import referral_button_call
from messages import BUTTONS


def get_referral_button(language: str):
    question_keyboard = InlineKeyboardMarkup()
    question_button = InlineKeyboardButton(text=BUTTONS[f'do_it_{language}'],
                                           callback_data=referral_button_call.new(referral='100friends',
                                                                                  value=language))
    question_keyboard.add(question_button)
    return question_keyboard
