from aiogram.types import CallbackQuery
from aiogram import types
from bot import dp, bot
from keyboards.inline.callback_datas import set_language
from db_operation import edit_language, get_user_questions_available, update_time_visit, get_random_question
from messages import MESSAGE
from config import PAY_SITE_ADDRESS


@dp.callback_query_handler(set_language.filter(language='language'))
async def set_language(call: CallbackQuery, callback_data: dict):
    telegram_id = call.from_user.id
    user_name = call.from_user.full_name
    user_name = user_name.replace(' ', '_')
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_language = callback_data.get('value')
    question_limit = get_user_questions_available(telegram_id)

    edit_language(telegram_id, user_language)

    if user_language == 'KZ':
        language_ok_message = MESSAGE['language_set_ok_kz']
        language_pay_message = MESSAGE['pay_kz']
        limit_error_message = MESSAGE['limit_error_kz']
    else:
        language_ok_message = MESSAGE['language_set_ok_ru']
        language_pay_message = MESSAGE['pay_ru']
        limit_error_message = MESSAGE['limit_error_ru']

    await call.answer(language_ok_message, cache_time=1)
    await call.message.edit_reply_markup()
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=language_ok_message)

    if question_limit > 0:
        question = get_random_question(user_language)

        # if question.image_code:
        #     await bot.send_photo(telegram_id, question.image_code)

        await bot.send_poll(telegram_id,
                            type='quiz',
                            is_anonymous=False,
                            is_closed=False,
                            question=question['question'],
                            options=question['options'],
                            correct_option_id=question['correct_option_id'],
                            explanation=question['explanation'])
    else:
        markup = types.InlineKeyboardMarkup()
        pay_link = types.InlineKeyboardButton(text=language_pay_message, url=PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={user_name}')
        markup.add(pay_link)
        await call.message.answer(limit_error_message, reply_markup=markup)
    update_time_visit(telegram_id)
