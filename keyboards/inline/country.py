from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_country

country_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇷🇺 РОССИЯ',
                                 callback_data=set_country.new(language='country', value='RU')),
            InlineKeyboardButton(text='🇰🇿 қазақстан',
                                 callback_data=set_country.new(language='country', value='KZ'))
        ]
    ]
)
