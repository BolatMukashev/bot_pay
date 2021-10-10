from aiogram.types import CallbackQuery
from bot import dp
from keyboards.inline.callback_datas import referral_button_call
from db_operations import get_user_language
from messages import PROMOTIONS
import config


@dp.callback_query_handler(referral_button_call.filter(referral='100friends'))
async def referral_button_handler(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_language = get_user_language(telegram_id)
    await call.message.answer(PROMOTIONS[f'100friends_action_message1_{user_language}'])
    await call.message.answer(PROMOTIONS[f'100friends_action_message2_{user_language}'] + "\n" +
                              f'{config.BOT_ADDRESS}?start={telegram_id}')
