from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import get_penalty
from messages import PENALTY

penalty_buttons = InlineKeyboardMarkup()

small_title_list = []
for el in PENALTY['items']:
    small_title_list.append(el['small_title'])

for el_id, el in enumerate(small_title_list):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id))
    penalty_buttons.add(button)
