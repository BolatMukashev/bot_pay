from aiogram.types import CallbackQuery
from bot import dp
from keyboards.inline.penalty_RU import *
from keyboards.inline.penalty_KZ import *
from messages import PENALTY
from db_operation import get_user_language


@dp.callback_query_handler(get_penalty.filter(type='penalty'))
async def get_penalty(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    language = get_user_language(telegram_id)
    answer_id = int(callback_data.get('value'))
    values = PENALTY[f'penalty_{language}']['items'][answer_id]
    text = [values['title']] + values['answers']
    text.append(values['description'])
    await call.message.answer('\n\n'.join(text))


@dp.callback_query_handler(next_penalty.filter(type='lty'))
async def edit_penalty(call: CallbackQuery, callback_data: dict):
    position = int(callback_data.get('position'))
    if position == 1:
        await call.message.edit_reply_markup(penalty_buttons_ru_1)
    elif position == 2:
        await call.message.edit_reply_markup(penalty_buttons_ru_2)
    if position == 3:
        await call.message.edit_reply_markup(penalty_buttons_ru_3)
    elif position == 4:
        await call.message.edit_reply_markup(penalty_buttons_ru_4)
    elif position == 5:
        await call.message.edit_reply_markup(penalty_buttons_ru_5)
    else:
        pass


@dp.callback_query_handler(next_penalty.filter(type='kzt'))
async def edit_penalty(call: CallbackQuery, callback_data: dict):
    position = int(callback_data.get('position'))
    if position == 1:
        await call.message.edit_reply_markup(penalty_buttons_kz_1)
    elif position == 2:
        await call.message.edit_reply_markup(penalty_buttons_kz_2)
    if position == 3:
        await call.message.edit_reply_markup(penalty_buttons_kz_3)
    elif position == 4:
        await call.message.edit_reply_markup(penalty_buttons_kz_4)
    elif position == 5:
        await call.message.edit_reply_markup(penalty_buttons_kz_5)
    else:
        pass
