from aiogram.types import CallbackQuery
from aiogram import types
from bot import dp, bot
from keyboards.inline.callback_datas import get_penalty, next_penalty
from keyboards.inline.penalty import *
from messages import PENALTY


@dp.callback_query_handler(get_penalty.filter(type='penalty'))
async def get_penalty(call: CallbackQuery, callback_data: dict):
    answer_id = int(callback_data.get('value'))
    values = PENALTY['items'][answer_id]
    text = [values['title']] + values['answers']
    text.append(values['description'])
    await call.message.answer('\n\n'.join(text))


@dp.callback_query_handler(next_penalty.filter(type='lty'))
async def edit_penalty(call: CallbackQuery, callback_data: dict):
    position = int(callback_data.get('position'))
    if position == 1:
        await call.message.edit_reply_markup(penalty_buttons1)
    elif position == 2:
        await call.message.edit_reply_markup(penalty_buttons2)
    if position == 3:
        await call.message.edit_reply_markup(penalty_buttons3)
    elif position == 4:
        await call.message.edit_reply_markup(penalty_buttons4)
    elif position == 5:
        await call.message.edit_reply_markup(penalty_buttons5)
    else:
        pass
