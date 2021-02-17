from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import dp
from keyboards.inline.callback_datas import russia_pen_titles, russia_pen_buttons, next_penalty, go_back_penalty
from keyboards.inline.penalty_RUSSIA import russian_penalty_titles
from messages import PENALTY_RUSSIA, BUTTONS


@dp.callback_query_handler(russia_pen_titles.filter(type='rus_penalty_1lvl'))
async def set_rus_penalty_values(call: CallbackQuery, callback_data: dict):
    type_id = int(callback_data.get('type_id'))
    russian_penalty_values = InlineKeyboardMarkup()
    for element in PENALTY_RUSSIA['values'][type_id]:
        for el_id, el in enumerate(PENALTY_RUSSIA['values'][type_id][element]):
            new_button = InlineKeyboardButton(text=el['simple_title'],
                                              callback_data=russia_pen_buttons.new(type='rus_penalty_2lvl',
                                                                                   type_id=type_id,
                                                                                   value_id=el_id))
            russian_penalty_values.add(new_button)
    button_back = InlineKeyboardButton(text=BUTTONS['back_RU'],
                                       callback_data=go_back_penalty.new(type='go_back', position=0))
    button_void = InlineKeyboardButton(text='⠀', callback_data=next_penalty.new(type='lty', position=9))
    russian_penalty_values.row(button_back, button_void, button_void)
    await call.message.edit_reply_markup(russian_penalty_values)


@dp.callback_query_handler(russia_pen_buttons.filter(type='rus_penalty_2lvl'))
async def set_rus_penalty_values(call: CallbackQuery, callback_data: dict):
    type_id = int(callback_data.get('type_id'))
    penalty_type = list(PENALTY_RUSSIA['values'][type_id].keys())[0]
    value_id = int(callback_data.get('value_id'))
    answer = PENALTY_RUSSIA['values'][type_id][penalty_type][value_id]
    message = f'{answer["title"]}\n\nШтраф:\n{answer["penalty"]}'
    await call.message.answer(message)


@dp.callback_query_handler(go_back_penalty.filter(type='go_back'))
async def go_back_penalty_fun(call: CallbackQuery):
    await call.message.edit_reply_markup(russian_penalty_titles)
