from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import set_language
from messages import BUTTONS

language_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTONS['lang_RU'],
                                 callback_data=set_language.new(language='language', value='RU')),
            InlineKeyboardButton(text=BUTTONS['lang_KZ'],
                                 callback_data=set_language.new(language='language', value='KZ'))
        ]
    ]
)
