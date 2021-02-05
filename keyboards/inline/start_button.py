from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import start_button_call

START_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='СТАРТ',
                                 callback_data=start_button_call.new(st='st', start='start'))
        ]
    ]
)
