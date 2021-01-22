from aiogram.types import CallbackQuery
from aiogram import types
from bot import dp, bot
from keyboards.inline.callback_datas import get_penalty
from messages import PENALTY


@dp.callback_query_handler(get_penalty.filter(type='penalty'))
async def get_penalty(call: CallbackQuery, callback_data: dict):
    answer_id = int(callback_data.get('value'))
    values = PENALTY['items'][answer_id]
    text = [values['title']] + values['answers']
    text.append(values['description'])
    await call.message.answer('\n'.join(text))
