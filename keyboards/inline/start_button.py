from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import start_button_call
from messages import BUTTONS

START_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTONS['start'],
                                 callback_data=start_button_call.new(start='start', value='None'))
        ]
    ]
)
