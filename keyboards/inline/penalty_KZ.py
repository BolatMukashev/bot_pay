from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import get_penalty, next_penalty
from messages import BUTTONS
from db_operations import get_data_from_json_file

language = 'KZ'
button_type = 'kzt'

data = get_data_from_json_file(f'backup/penalty_kazakhstan_{language}.json')

small_title_list = []
for el in data['items']:
    small_title_list.append(el['small_title'])


penalty_buttons_kz_1 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[:7]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id))
    penalty_buttons_kz_1.add(button)
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type=button_type, position=9))
button_next = InlineKeyboardButton(text=BUTTONS[f'next_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=2))
penalty_buttons_kz_1.row(button_void, button_void, button_next)


penalty_buttons_kz_2 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[7:14]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+7))
    penalty_buttons_kz_2.add(button)
button_back = InlineKeyboardButton(text=BUTTONS[f'back_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=1))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type=button_type, position=9))
button_next = InlineKeyboardButton(text=BUTTONS[f'next_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=3))
penalty_buttons_kz_2.row(button_back, button_void, button_next)


penalty_buttons_kz_3 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[14:21]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+14))
    penalty_buttons_kz_3.add(button)
button_back = InlineKeyboardButton(text=BUTTONS[f'back_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=2))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type=button_type, position=9))
button_next = InlineKeyboardButton(text=BUTTONS[f'next_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=4))
penalty_buttons_kz_3.row(button_back, button_void, button_next)


penalty_buttons_kz_4 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[21:28]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+21))
    penalty_buttons_kz_4.add(button)
button_back = InlineKeyboardButton(text=BUTTONS[f'back_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=3))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type=button_type, position=9))
button_next = InlineKeyboardButton(text=BUTTONS[f'next_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=5))
penalty_buttons_kz_4.row(button_back, button_void, button_next)


penalty_buttons_kz_5 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[28:]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+28))
    penalty_buttons_kz_5.add(button)
button_back = InlineKeyboardButton(text=BUTTONS[f'back_{language}'],
                                   callback_data=next_penalty.new(type=button_type, position=4))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type=button_type, position=9))
penalty_buttons_kz_5.row(button_back, button_void, button_void)
