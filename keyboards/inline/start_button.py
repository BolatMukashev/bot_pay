from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import start_button_call
from messages import BUTTONS

start_keyboard = InlineKeyboardMarkup()
start_button = InlineKeyboardButton(text=BUTTONS['start'],
                                    callback_data=start_button_call.new(start='start', value='None'))
start_keyboard.add(start_button)
