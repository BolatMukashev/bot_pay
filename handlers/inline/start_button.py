from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import start_button_call
from db_operation import get_random_question, update_registration_status, get_user_language
import config


@dp.callback_query_handler(start_button_call.filter(start='start'))
async def start_button_handler(call: CallbackQuery):
    telegram_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_language = get_user_language(telegram_id)

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    update_registration_status(telegram_id)

    question = get_random_question(user_language)
    if config.DEBUG is False and question['image_code']:
        await bot.send_photo(telegram_id, question['image_code'])
    await bot.send_poll(telegram_id,
                        type='quiz',
                        is_anonymous=False,
                        is_closed=False,
                        question=question['question'],
                        options=question['options'],
                        correct_option_id=question['correct_option_id'],
                        explanation=question['explanation'])
