from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import get_penalty, next_penalty
from messages import PENALTY, BUTTONS

small_title_list = []
for el in PENALTY['items']:
    small_title_list.append(el['small_title'])


penalty_buttons1 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[:7]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id))
    penalty_buttons1.add(button)
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
button_next = InlineKeyboardButton(text=BUTTONS['next_RU'], callback_data=next_penalty.new(type='lty', position=2))
penalty_buttons1.row(button_void, button_void, button_next)


penalty_buttons2 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[7:14]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+7))
    penalty_buttons2.add(button)
button_back = InlineKeyboardButton(text=BUTTONS['back_RU'], callback_data=next_penalty.new(type='lty', position=1))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
button_next = InlineKeyboardButton(text=BUTTONS['next_RU'], callback_data=next_penalty.new(type='lty', position=3))
penalty_buttons2.row(button_back, button_void, button_next)


penalty_buttons3 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[14:21]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+14))
    penalty_buttons3.add(button)
button_back = InlineKeyboardButton(text=BUTTONS['back_RU'], callback_data=next_penalty.new(type='lty', position=2))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
button_next = InlineKeyboardButton(text=BUTTONS['next_RU'], callback_data=next_penalty.new(type='lty', position=4))
penalty_buttons3.row(button_back, button_void, button_next)


penalty_buttons4 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[21:28]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+21))
    penalty_buttons4.add(button)
button_back = InlineKeyboardButton(text=BUTTONS['back_RU'], callback_data=next_penalty.new(type='lty', position=3))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
button_next = InlineKeyboardButton(text=BUTTONS['next_RU'], callback_data=next_penalty.new(type='lty', position=5))
penalty_buttons4.row(button_back, button_void, button_next)


penalty_buttons5 = InlineKeyboardMarkup()
for el_id, el in enumerate(small_title_list[28:]):
    button = InlineKeyboardButton(text=el, callback_data=get_penalty.new(type='penalty', value=el_id+28))
    penalty_buttons5.add(button)
button_back = InlineKeyboardButton(text=BUTTONS['back_RU'], callback_data=next_penalty.new(type='lty', position=4))
button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
penalty_buttons5.row(button_back, button_void, button_void)
