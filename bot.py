from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound
from db_operation import *
from keyboards.inline.language import language_buttons
from keyboards.inline.penalty_RU import penalty_buttons_ru_1
from keyboards.inline.penalty_KZ import penalty_buttons_kz_1
from keyboards.inline.penalty_RUSSIA import russian_penalty_titles
from messages import *
from gmail import send_emails_to_schools
import io
from static.html_messages.hello_auto_school import hello_auto_school_message
from static.html_messages.new_functions_and_offers import new_func_and_offers_message


if config.DEBUG:
    bot = Bot(token=config.TEST_BOT_TOKEN)
else:
    bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


class AllStates(StatesGroup):
    MessageForAll: State = State()
    MessageForAllRepair: State = State()
    SendPromotionalPost: State = State()
    UsePromoCode: State = State()
    DeleteAutoSchool: State = State()
    SendEmailToAllAutoSchools: State = State()


@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        commands = [types.BotCommand(command="/question", description="Новый вопрос. Жаңа сұрақ"),
                    types.BotCommand(command="/language", description="Изменить язык. Тілді өзгерту"),
                    types.BotCommand(command="/penalty", description="Посмотреть штрафы. Айыппұлдарды қарау"),
                    types.BotCommand(command="/promo_code", description="Использовать промокод. Промокодты қолдану"),
                    types.BotCommand(command="/pay", description="Оплатить. Төлеу"),
                    types.BotCommand(command="/info", description="Подсказки. Кеңестер")]
        await bot.set_my_commands(commands)
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    new_user(telegram_id, full_name)

    users_list_14 = get_loser_list_14days()
    for user_id in users_list_14:
        user_language = get_user_language(user_id)

        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + '?' + f'telegram_id={telegram_id}'
        pay_button_text = BUTTONS[f'pay_{user_language}']
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)

        await bot.send_sticker(user_id, STICKERS['come_back'])
        await bot.send_message(user_id, OFFERS[f'second_week_promotional_offer_{user_language}'], reply_markup=markup)

        change_price_in_rubles_on_user(user_id, config.PRICE_AFTER_14DAYS)
        update_second_week_promotional_offer_status(user_id)

    users_list_45 = get_loser_list_45days()
    for user_id in users_list_45:
        user_language = get_user_language(user_id)

        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + '?' + f'telegram_id={telegram_id}'
        pay_button_text = BUTTONS[f'pay_{user_language}']
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)

        await bot.send_sticker(user_id, STICKERS['come_back'])
        await bot.send_message(user_id, OFFERS[f'sixth_week_promotional_offer_{user_language}'], reply_markup=markup)

        change_price_in_rubles_on_user(user_id, config.PRICE_AFTER_45DAYS)
        update_sixth_week_promotional_offer_status(user_id)

    await bot.send_sticker(telegram_id, STICKERS['hello'])
    await message.answer(MESSAGE['start_user_text'])
    if not get_user_registration_status(telegram_id):
        await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["question"])
async def command_question(message: types.Message):
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    if telegram_id == config.ADMIN_ID:
        await message.answer(MESSAGE['start_admin_text'])
    if not user_time_limit_is_over(telegram_id):
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
    else:
        limit_error_message = MESSAGE[f'limit_error_{user_language}']
        pay_button_text = BUTTONS[f'pay_{user_language}']

        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + '?' + f'telegram_id={telegram_id}'
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)
        await bot.send_message(telegram_id, limit_error_message, reply_markup=markup)
    update_time_visit(telegram_id)


@dp.message_handler(commands=["language"])
async def command_language(message: types.Message):
    await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["penalty"])
async def command_penalty(message: types.Message):
    telegram_id = message.from_user.id
    language = get_user_language(telegram_id)
    country = get_user_country(telegram_id)
    if country == 'RU':
        await message.answer(PENALTY_RUSSIA['title'], reply_markup=russian_penalty_titles)
    else:
        if language == 'RU':
            await message.answer(PENALTY[f'penalty_{language}']['title'], reply_markup=penalty_buttons_ru_1)
        if language == 'KZ':
            await message.answer(PENALTY[f'penalty_{language}']['title'], reply_markup=penalty_buttons_kz_1)


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


@dp.message_handler(state=AllStates.MessageForAll, content_types=types.ContentTypes.TEXT)
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


@dp.message_handler(commands=["send_email_for_all_auto_schools"], state='*')
async def command_send_email_for_all_auto_schools(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Отправь сообщение в виде HTML кода, но помни что оно уйдет всем Автошколам!!!')
        await AllStates.SendEmailToAllAutoSchools.set()


@dp.message_handler(state=AllStates.SendEmailToAllAutoSchools, content_types=types.ContentTypes.TEXT)
async def command_send_email_for_all_auto_schools_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    emails = get_all_auto_schools_emails()
    message_subtitle = 'Произошли изменения'
    html = new_func_and_offers_message(my_message)
    send_emails_to_schools(emails, message_subtitle, html)
    await message.answer('Сообщения о изменениях были отправлены автошколам!')
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


@dp.message_handler(state=AllStates.MessageForAllRepair, content_types=types.ContentTypes.TEXT)
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


@dp.message_handler(commands=["delete_auto_school"], state='*')
async def command_delete_auto_school(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Напиши секретный ключ автошколы:')
        await AllStates.DeleteAutoSchool.set()


@dp.message_handler(state=AllStates.DeleteAutoSchool, content_types=types.ContentTypes.TEXT)
async def command_delete_auto_school_action(message: types.Message, state: FSMContext):
    secret_key = message.text
    await state.update_data(secret_key=secret_key)
    delete_auto_schools_by(secret_key)
    await message.answer('Автошкола успешно удалена из базы!')
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
async def command_all_promo_codes(message: types.Message):
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_all_promo_code_list()
        await message.answer(result)


@dp.message_handler(commands=["promo_code"], state='*')
async def command_promo_code(message: types.Message):
    telegram_id = message.from_user.id
    language = get_user_language(telegram_id)
    user_promo_code_used_status = get_user_promo_code_used_status(telegram_id)
    if not user_promo_code_used_status:
        await message.answer(PROMO_CODE[f'promo_code_command_text_{language}'])
        await AllStates.UsePromoCode.set()
    else:
        await message.answer_sticker(STICKERS['NO'])
        await message.answer(PROMO_CODE[f'promo_code_was_used_{language}'])


@dp.message_handler(state=AllStates.UsePromoCode, content_types=types.ContentTypes.TEXT)
async def command_promo_code_action(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    language = get_user_language(telegram_id)
    user_promo_code = message.text.upper()
    await state.update_data(user_promo_code=user_promo_code)
    promo_codes = all_promo_codes()
    if user_promo_code in promo_codes:
        up_user_time_limit_7days(telegram_id)
        up_number_of_references(user_promo_code)
        update_user_promo_code_used_status(telegram_id)
        change_price_in_rubles_on_user(telegram_id, config.PRICE_AFTER_14DAYS)
        await message.answer_sticker(STICKERS['all_good'])
        await message.answer(PROMO_CODE[f'promo_code_activated_{language}'])
    else:
        await message.answer_sticker(STICKERS['NO'])
        await message.answer(PROMO_CODE[f'promo_code_error_{language}'])
    await state.finish()


@dp.message_handler(commands=["pay"])
async def command_pay(message: types.Message):
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    monetary_unit = get_monetary_unit_by_user_country(telegram_id)
    price = get_finally_price(telegram_id)
    pay_message_text = MESSAGE[f'pay_message_{user_language}'] + f' {str(price)} {monetary_unit}!'

    markup = types.InlineKeyboardMarkup()
    url = config.PAY_SITE_ADDRESS + '?' + f'telegram_id={telegram_id}'
    pay_button = BUTTONS[f'pay_{user_language}']
    pay_link = types.InlineKeyboardButton(text=pay_button, url=url)
    markup.add(pay_link)

    await message.answer(pay_message_text, reply_markup=markup)


@dp.message_handler(commands=["info"])
async def command_help(message: types.Message):
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'info_{user_language}'])


@dp.message_handler(commands=["send_hello_emails_to_new_schools"])
async def command_send_hello_emails_to_new_schools(message: types.Message):
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        schools = get_not_notified_auto_schools()
        for school in schools:
            school_id = school.id
            secret_key = school.secret_key
            emails = pickle.loads(school.emails)
            sub_title = 'Новая образовательная платформа'
            html = hello_auto_school_message(secret_key)
            send_emails_to_schools(emails, sub_title, html)
            edit_notified_status(school_id)
        await message.answer('Приветственные сообщения автошколам были отправлены!')


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    telegram_id = quiz_answer.user.id
    user_language = get_user_language(telegram_id)
    if not user_time_limit_is_over(telegram_id):
        question = get_random_question(user_language)
        if config.DEBUG is False and question['image_code']:
            await bot.send_photo(telegram_id, question['image_code'])
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

        markup = types.InlineKeyboardMarkup()
        url = config.PAY_SITE_ADDRESS + '?' + f'telegram_id={telegram_id}'
        pay_button_text = BUTTONS[f'pay_{user_language}']
        pay_link = types.InlineKeyboardButton(text=pay_button_text, url=url)
        markup.add(pay_link)
        await bot.send_message(telegram_id, limit_error_message, reply_markup=markup)
    update_time_visit(telegram_id)


@dp.message_handler(content_types=['document'])
async def scan_message(message: types.Message):
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        document = message.document.file_id
        file = await bot.download_file_by_id(document)
        data = json.load(io.TextIOWrapper(file, encoding='utf-8'))
        try:
            set_auto_schools_in_db(data)
            await message.answer('Информация об автошколах была добавлена в базу...')
        except KeyError:
            await message.answer('Не корректный набор данных!')


if __name__ == "__main__":
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
