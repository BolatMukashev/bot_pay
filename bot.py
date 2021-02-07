from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound
from db_operation import *
from keyboards.inline.language import language_buttons
from keyboards.inline.penalty import penalty_buttons1
from messages import MESSAGE, PENALTY, STICKERS, BUTTONS, OFFERS

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class AllStates(StatesGroup):
    MessageForAll: State = State()
    MessageForAllRepair: State = State()
    SendPromotionalPost: State = State()


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        commands = [types.BotCommand(command="/question", description="Старт"),
                    types.BotCommand(command="/language", description="Изменить язык. Тілді өзгерту"),
                    types.BotCommand(command="/penalty", description="Посмотрить штрафы"),
                    types.BotCommand(command="/promo_code", description="Использовать промокод. Промокодты қолдану"),
                    types.BotCommand(command="/pay", description="Оплатить. Төлеу"),
                    types.BotCommand(command="/info", description="Подсказки")]
        await bot.set_my_commands(commands)
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    telegram_id = message.from_user.id
    user_name = message.from_user.full_name
    new_user(telegram_id, user_name)

    users_list_14 = get_loser_list_14days()
    for user_id in users_list_14:
        user_name = get_user_name_by(user_id)
        name_to_request = user_name.replace(' ', '_')
        user_language = get_user_language(user_id)
        pay_button_text = BUTTONS[f'pay_{user_language}']
        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={name_to_request}'
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)
        await bot.send_sticker(user_id, STICKERS['come_back'])
        await bot.send_message(user_id, OFFERS[f'second_week_promotional_offer_{user_language}'], reply_markup=markup)
        change_price_in_rubles_on_user(user_id, config.PRICE_AFTER_14DAYS)
        update_second_week_promotional_offer_status(user_id)

    users_list_45 = get_loser_list_45days()
    for user_id in users_list_45:
        user_name = get_user_name_by(user_id)
        name_to_request = user_name.replace(' ', '_')
        user_language = get_user_language(user_id)
        pay_button_text = BUTTONS[f'pay_{user_language}']
        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={name_to_request}'
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)
        await bot.send_sticker(user_id, STICKERS['come_back'])
        await bot.send_message(user_id, OFFERS[f'sixth_week_promotional_offer_{user_language}'], reply_markup=markup)
        change_price_in_rubles_on_user(user_id, config.PRICE_AFTER_45DAYS)
        update_sixth_week_promotional_offer_status(user_id)

    await bot.send_sticker(telegram_id, STICKERS['hello'])
    if telegram_id == config.ADMIN_ID:
        await message.answer(MESSAGE['start_admin_text'])
    else:
        await message.answer(MESSAGE['start_user_text'])
        if not user_registration_is_over(telegram_id):
            await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["language"])
async def command_language(message: types.Message):
    await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["penalty"])
async def command_penalty(message: types.Message):
    await message.answer(PENALTY['title'], reply_markup=penalty_buttons1)


@dp.message_handler(commands=["statistics"])
async def command_statistics(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_big_statistics()
        await message.answer(result)


@dp.message_handler(commands=["message_for_all"], state='*')
async def command_message_for_all(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Пиши своё сообщение, но помни что оно уйдет всем пользователям!!!')
        await AllStates.MessageForAll.set()


@dp.message_handler(state=AllStates.MessageForAll,  content_types=types.ContentTypes.TEXT)
async def command_message_for_all_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    users = all_users_id()
    for user in users:
        try:
            await bot.send_sticker(user, STICKERS['message'])
            await bot.send_message(user, my_message)
        except ChatNotFound:
            pass
    await state.finish()


@dp.message_handler(commands=["send_promotional_post"], state='*')
async def command_send_photo(message: types.Message):
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer('Отправь рекламное фото и сообщение, оно будет перенаправлено всем пользователям!')
        await AllStates.SendPromotionalPost.set()


@dp.message_handler(state=AllStates.SendPromotionalPost, content_types=['text', 'photo'])
async def command_send_photo_action(message: types.Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    my_message = message.caption
    await state.update_data(photo_id=photo_id)
    all_users = all_users_id()
    for user_id in all_users:
        try:
            await bot.send_photo(user_id, photo_id, caption=my_message)
        except ChatNotFound:
            pass
    await state.finish()


@dp.message_handler(commands=["message_for_all_about_repair"], state='*')
async def command_message_for_all_repair(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Пиши своё сообщение о РЕМОНТНЫХ РАБОТАХ, но помни что оно уйдет всем пользователям!!!')
        await AllStates.MessageForAllRepair.set()


@dp.message_handler(state=AllStates.MessageForAllRepair,  content_types=types.ContentTypes.TEXT)
async def command_message_for_all_repair_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    users = all_users_id()
    for user in users:
        try:
            await bot.send_sticker(user, STICKERS['repair'])
            await bot.send_message(user, my_message)
        except ChatNotFound:
            pass
    await state.finish()


@dp.message_handler(commands=["up_admin_time_limit"])
async def command_up_admin_q_a(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        up_admin_time_limit_3minute()
        await message.answer('+3 минуты добавлено')


@dp.message_handler(commands=["all_users"])
async def command_all_users(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_all_users_list()
        await message.answer(result)


@dp.message_handler(commands=["all_promo_codes"])
async def command_all_users(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_all_promo_code_list()
        await message.answer(result)


@dp.message_handler(commands=["pay"])
async def command_user_do_pay(message: types.Message):
    telegram_id = message.from_user.id
    user_name = message.from_user.full_name
    user_name = user_name.replace(' ', '_')
    user_language = get_user_language(telegram_id)
    pay_text = MESSAGE[f'pay_message_{user_language}']
    language_pay_message = MESSAGE[f'pay_{user_language}']

    markup = types.InlineKeyboardMarkup()
    url = config.PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={user_name}'
    pay_link = types.InlineKeyboardButton(text=language_pay_message, url=url)
    markup.add(pay_link)
    await message.answer(pay_text, reply_markup=markup)


@dp.message_handler(commands=["info"])
async def command_help(message: types.Message):
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'info_{user_language}'])


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    telegram_id = quiz_answer.user.id
    user_name = quiz_answer.user.full_name
    name_to_request = user_name.replace(' ', '_')
    user_language = get_user_language(telegram_id)
    if not user_time_limit_is_over(telegram_id):
        question = get_random_question(user_language)
        if config.DEBUG is False and question.image_code:
            await bot.send_photo(telegram_id, question.image_code)
        await quiz_answer.bot.send_poll(telegram_id,
                                        type='quiz',
                                        is_anonymous=False,
                                        is_closed=False,
                                        question=question['question'],
                                        options=question['options'],
                                        correct_option_id=question['correct_option_id'],
                                        explanation=question['explanation'])
    else:
        limit_error_message = MESSAGE[f'limit_error_{user_language}']
        pay_button_text = BUTTONS[f'pay_{user_language}']

        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + f'?language={user_language}&telegram_id={telegram_id}&user_name={name_to_request}'
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)
        await bot.send_message(telegram_id, limit_error_message, reply_markup=markup)
    update_time_visit(telegram_id)


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
