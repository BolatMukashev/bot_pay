from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import set_country
from messages import BUTTONS

country_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTONS['russia'],
                                 callback_data=set_country.new(language='country', value='RU')),
            InlineKeyboardButton(text=BUTTONS['kazakhstan'],
                                 callback_data=set_country.new(language='country', value='KZ'))
        ]
    ]
)
