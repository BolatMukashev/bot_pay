from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import set_country
from db_operation import edit_user_country, get_user_language, get_random_question
from config import DEBUG


@dp.callback_query_handler(set_country.filter(country='country'))
async def update_country(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_country = callback_data.get('value')
    edit_user_country(telegram_id, user_country)
    user_language = get_user_language(telegram_id)

    await call.message.edit_reply_markup()
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    question = get_random_question(user_language)
    if DEBUG is False and question.image_code:
        await bot.send_photo(telegram_id, question.image_code)
    await bot.send_poll(telegram_id,
                        type='quiz',
                        is_anonymous=False,
                        is_closed=False,
                        question=question['question'],
                        options=question['options'],
                        correct_option_id=question['correct_option_id'],
                        explanation=question['explanation'])
