from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import russia_pen_titles, russia_pen_buttons
from messages import PENALTY_RUSSIA

button_type = 'lty'

small_title_list = [list(x.keys())[0] for x in PENALTY_RUSSIA['values']]

russian_penalty_titles = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list):
    button = InlineKeyboardButton(text=el, callback_data=russia_pen_titles.new(type='rus_penalty_1lvl', type_id=el_id))
    russian_penalty_titles.add(button)
