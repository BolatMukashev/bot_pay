from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import pay_page_link

pay_button_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Оплатить',
                                 callback_data=pay_page_link.new(value='fdsfdf'),
                                 url='https://habrahabr.ru')
        ]
    ]
)
