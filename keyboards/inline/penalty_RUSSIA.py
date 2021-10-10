from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import russia_pen_titles
from db_operations import get_data_from_json_file

data = get_data_from_json_file('backup/penalty_russia.json')

button_type = 'lty'

small_title_list = [list(x.keys())[0] for x in data['values']]

russian_penalty_titles = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list):
    button = InlineKeyboardButton(text=el, callback_data=russia_pen_titles.new(type='rus_penalty_1lvl', type_id=el_id))
    russian_penalty_titles.add(button)
