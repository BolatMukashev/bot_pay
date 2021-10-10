from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import set_country
from keyboards.inline.start_button import START_button
from db_operations import edit_user_country, get_user_language
from messages import MESSAGE
from db_operations import get_user_registration_status


@dp.callback_query_handler(set_country.filter(country='country'))
async def update_country(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_country = callback_data.get('value')
    edit_user_country(telegram_id, user_country)
    user_language = get_user_language(telegram_id)

    await call.answer(MESSAGE[f'country_edited_ok_{user_language}'], cache_time=1)
    await call.message.edit_reply_markup()
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text=MESSAGE[f'country_edited_ok_{user_language}'])
    if not get_user_registration_status(telegram_id):
        await bot.send_message(chat_id,
                               text=MESSAGE[f'registration_ok_{user_language}'],
                               reply_markup=START_button,
                               parse_mode='HTML')
