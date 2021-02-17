from aiogram.utils.callback_data import CallbackData

set_language = CallbackData('lang', 'language', 'value')
set_country = CallbackData('count', 'country', 'value')
get_penalty = CallbackData('penalty', 'type', 'value')
russia_pen_titles = CallbackData('rus_penalty', 'type', 'type_id')
russia_pen_buttons = CallbackData('rus_penalty', 'type', 'type_id', 'value_id')
next_penalty = CallbackData('penalty', 'type', 'position')
go_back_penalty = CallbackData('penalty', 'type', 'position')
start_button_call = CallbackData('st', 'start', 'value')
