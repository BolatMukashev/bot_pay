from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import set_language
from db_operation import edit_user_language, get_user_registration_status
from keyboards.inline.country import country_buttons
from messages import MESSAGE


@dp.callback_query_handler(set_language.filter(language='language'))
async def update_language(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_language = callback_data.get('value')
    edit_user_language(telegram_id, user_language)
    language_ok_message = MESSAGE[f'language_set_ok_{user_language}']

    await call.answer(language_ok_message, cache_time=1)
    await call.message.edit_reply_markup()
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=language_ok_message)
    if not get_user_registration_status(telegram_id):
        await bot.send_message(chat_id, text=MESSAGE[f'country_choice_{user_language}'], reply_markup=country_buttons)
