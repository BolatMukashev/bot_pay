from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import set_language

language_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇷🇺 Русский язык',
                                 callback_data=set_language.new(language='language', value='RU')),
            InlineKeyboardButton(text='🇰🇿 Қазақ тілі',
                                 callback_data=set_language.new(language='language', value='KZ'))
        ]
    ]
)
