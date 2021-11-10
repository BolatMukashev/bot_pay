from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import question_button_call
from messages import BUTTONS


def get_question_button(language: str):
    question_keyboard = InlineKeyboardMarkup(row_width=8)
    question_button = InlineKeyboardButton(text=BUTTONS[f'get_question_{language}'],
                                           callback_data=question_button_call.new(question='question', value='None'))
    question_keyboard.add(question_button)
    return question_keyboard
