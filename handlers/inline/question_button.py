from aiogram.types import CallbackQuery
from bot import dp, bot
from keyboards.inline.callback_datas import question_button_call
from db_operations import get_random_question, update_registration_status, get_user_language
import config
import pickle
import random
from messages import STICKERS, MESSAGE
from db_operations import user_time_limit_is_over, update_time_visit


@dp.callback_query_handler(question_button_call.filter(question='question'))
async def question_button_handler(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_language = get_user_language(telegram_id)

    if not user_time_limit_is_over(telegram_id):
        question = get_random_question(user_language)
        if config.DEBUG is False and question.image_code:
            await bot.send_photo(telegram_id, question.image_code)
        options = pickle.loads(question.all_answers)
        random.shuffle(options)
        correct_option_id = options.index(question.correct_answer)
        await bot.send_poll(telegram_id,
                            type='quiz',
                            is_anonymous=False,
                            is_closed=False,
                            question=question.question,
                            options=options,
                            correct_option_id=correct_option_id,
                            explanation=question.explanation)
    else:
        await bot.send_sticker(telegram_id, STICKERS['flower'])
        limit_error_message = MESSAGE[f'limit_error_{user_language}']
        await bot.send_message(telegram_id, limit_error_message)
    update_time_visit(telegram_id)
