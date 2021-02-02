from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import ChatNotFound
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import *
from db_operation import *
from keyboards.inline.language import language_buttons
from keyboards.inline.penalty import penalty_buttons
from messages import MESSAGE, PENALTY


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class AllStates(StatesGroup):
    MessageForAll: State = State()
    MessageForLosers: State = State()
    NewSuperPromoCode: State = State()


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        commands = [types.BotCommand(command="/start", description="Старт"),
                    types.BotCommand(command="/language", description="Изменить язык. Тілді өзгерту"),
                    types.BotCommand(command="/penalty", description="Посмотрить штрафы"),
                    types.BotCommand(command="/pay", description="Оплатить. Төлеу"),
                    types.BotCommand(command="/info", description="Подсказки")]
        await bot.set_my_commands(commands)
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    new_user(user_id, user_name)
    if user_id == ADMIN_ID:
        await message.answer(MESSAGE['start_admin'])
    else:
        await message.answer(MESSAGE['start_user'])
        await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["language"])
async def language(message: types.Message):
    await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["penalty"])
async def penalty(message: types.Message):
    await message.answer(PENALTY['main'], reply_markup=penalty_buttons)


@dp.message_handler(commands=["statistics"])
async def statistics(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        result = get_big_statistics()
        await message.answer(result)


@dp.message_handler(commands=["message_for_all"], state='*')
async def message_for_all(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer('Пиши своё сообщение, но помни что оно уйдет всем пользователям!!!')
        await AllStates.MessageForAll.set()


@dp.message_handler(state=AllStates.MessageForAll,  content_types=types.ContentTypes.TEXT)
async def message_for_all_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    users = all_users_id()
    for user in users:
        try:
            await bot.send_message(user, my_message)
        except ChatNotFound:
            pass
    await state.finish()


@dp.message_handler(commands=["message_for_losers"], state='*')
async def message_for_losers(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer('Сообщение получат те кто не заходил в бота 2 недели и не оплачивал сервис...')
        await AllStates.MessageForLosers.set()


@dp.message_handler(state=AllStates.MessageForLosers,  content_types=types.ContentTypes.TEXT)
async def message_for_losers_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    users = get_loser_list()
    for user in users:
        try:
            await bot.send_message(user, my_message)
        except ChatNotFound:
            pass
    await state.finish()
    await bot.send_message(ADMIN_ID, f'Сообщение отправлено {len(users)} пользователям.')


@dp.message_handler(commands=["super_promo_code"], state='*')
async def set_super_promo_code(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer('Новый супер-промо код:')
        await AllStates.NewSuperPromoCode.set()


@dp.message_handler(state=AllStates.NewSuperPromoCode,  content_types=types.ContentTypes.TEXT)
async def set_super_promo_code_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    edit_super_promo_code(my_message)
    await message.answer('Промокод установлен!')
    await state.finish()


@dp.message_handler(commands=["standard_super_promo_code"])
async def standard_super_promo_code(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        set_default_super_promo_code()
        await message.answer('Стандартный промокод установлен!')


@dp.message_handler(commands=["up_admin_q_a"])
async def up_admin_q_a(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        up_admin_questions_available()
        await message.answer('+5 к вопросам')


@dp.message_handler(commands=["all_users"])
async def all_users(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        result = view_all_users_list()
        await message.answer(result)


@dp.message_handler(commands=["all_promo_codes"])
async def all_users(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        result = view_all_promo_code_list()
        await message.answer(result)


@dp.message_handler(commands=["agreement_school_list"])
async def agreement_school_list(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        result = get_agreement_school_list()
        await message.answer('\n'.join(result))


@dp.message_handler(commands=["pay"])
async def user_do_pay(message: types.Message):
    telegram_id = message.from_user.id
    user_name = message.from_user.full_name
    user_name = user_name.replace(' ', '_')
    user_language = get_language(telegram_id)
    if user_language == 'KZ':
        pay_text = MESSAGE['pay_message_kz']
        language_pay_message = MESSAGE['pay_kz']
    else:
        pay_text = MESSAGE['pay_message_ru']
        language_pay_message = MESSAGE['pay_ru']

    markup = types.InlineKeyboardMarkup()
    pay_link = types.InlineKeyboardButton(text=language_pay_message,
                                          url=PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={user_name}')
    markup.add(pay_link)
    await message.answer(pay_text, reply_markup=markup)


@dp.message_handler(commands=["info"])
async def cmd_help(message: types.Message):
    telegram_id = message.from_user.id
    user_language = get_language(telegram_id)
    if user_language == 'KZ':
        await message.answer(MESSAGE['info_kz'])
    else:
        await message.answer(MESSAGE['info_ru'])


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    telegram_id = quiz_answer.user.id
    user_name = quiz_answer.user.full_name
    user_name = user_name.replace(' ', '_')
    question_limit = get_user_questions_available(telegram_id)
    user_language = get_language(telegram_id)
    if question_limit > 0:
        question = get_random_question(user_language)

        # if question.image_code:
        #     await bot.send_photo(telegram_id, question.image_code)

        await quiz_answer.bot.send_poll(telegram_id,
                                        type='quiz',
                                        is_anonymous=False,
                                        is_closed=False,
                                        question=question['question'],
                                        options=question['options'],
                                        correct_option_id=question['correct_option_id'],
                                        explanation=question['explanation'])
        reduce_user_questions_available(telegram_id)
    else:
        if user_language == 'KZ':
            language_pay_message = MESSAGE['pay_kz']
            limit_error_message = MESSAGE['limit_error_kz']
        else:
            language_pay_message = MESSAGE['pay_ru']
            limit_error_message = MESSAGE['limit_error_ru']

        markup = types.InlineKeyboardMarkup()
        pay_link = types.InlineKeyboardButton(text=language_pay_message,
                                              url=PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={user_name}')
        markup.add(pay_link)
        await bot.send_message(telegram_id, limit_error_message, reply_markup=markup)
    update_time_visit(telegram_id)


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)

