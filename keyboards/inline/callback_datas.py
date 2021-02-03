from aiogram.utils.callback_data import CallbackData

set_language = CallbackData('lang', 'language', 'value')
get_penalty = CallbackData('penalty', 'type', 'value')
next_penalty = CallbackData('penalty', 'type', 'position')
pay_page_link = CallbackData('pay', 'value')
