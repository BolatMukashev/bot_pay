from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked
from db_operations import *
from json_parser import parse_schools_from_object
from keyboards.inline.callback_datas import referral_button_call
from keyboards.inline.country import country_buttons
from keyboards.inline.language import language_buttons
from keyboards.inline.penalty_RU import penalty_buttons_ru_1
from keyboards.inline.penalty_KZ import penalty_buttons_kz_1
from keyboards.inline.penalty_RUSSIA import russian_penalty_titles
from messages import *
from gmail import send_emails_to_schools
import io
import asyncio
from pay_system_ioka import PayLinkIoka
from static.html_messages.hello_auto_school import hello_auto_school_message
from static.html_messages.new_functions_and_offers import new_func_and_offers_message
from tqdm import tqdm as loading_bar


token = config.TEST_BOT_TOKEN if config.DEBUG else config.BOT_TOKEN


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class AllStates(StatesGroup):
    MessageForAll: State = State()
    SendPromotionalPost: State = State()
    UsePromoCode: State = State()
    DeleteAutoSchool: State = State()
    SendEmailToAllAutoSchools: State = State()
    InfoAboutUser: State = State()


@dp.message_handler(commands=["set_commands"], state="*")
async def command_set_commands(message: types.Message):
    """Установить команды в боковом меню, в зависимости от языка"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        commands_list = ["set_commands", "set_commands_ru", "set_commands_kz"]
        for command in commands_list:
            descriptions = get_commands_descriptions_and_language_code(command)
            commands = [types.BotCommand(command="/question", description=descriptions['question']),
                        types.BotCommand(command="/penalty", description=descriptions['penalty']),
                        types.BotCommand(command="/pay", description=descriptions['pay']),
                        types.BotCommand(command="/promo_code", description=descriptions['promo_code']),
                        types.BotCommand(command="/promotions", description=descriptions['promotions']),
                        types.BotCommand(command="/certificate", description=descriptions['certificate']),
                        types.BotCommand(command="/donate", description=descriptions['donate']),
                        types.BotCommand(command="/chat", description=descriptions['chat']),
                        types.BotCommand(command="/error", description=descriptions['error']),
                        types.BotCommand(command="/language", description=descriptions['language']),
                        types.BotCommand(command="/country", description=descriptions['country']),
                        types.BotCommand(command="/info", description=descriptions['info'])]
            await bot.set_my_commands(commands=commands, language_code=descriptions['language_code'])
        await message.answer("Команды установлены!")


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    """Начало работы, приветственное сообщение и вызов меню регистрации пользователя"""
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    referral_telegram_id = message.get_args()

    up_daily_limit_to_referral(referral_telegram_id, telegram_id, 5)
    # check leavers and add to user and del in leaver
    if telegram_id not in get_all_leavers_telegram_id():
        add_user(telegram_id=telegram_id, full_name=full_name, referral=referral_telegram_id)
    await bot.send_sticker(telegram_id, STICKERS['hello'])
    await message.answer(MESSAGE['start_user_text'].format(full_name))
    if not get_user_registration_status(telegram_id):
        await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["question"])
async def command_question(message: types.Message):
    """Получить новый вопрос из базы"""
    telegram_id = message.from_user.id
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


@dp.message_handler(commands=["language"])
async def command_language(message: types.Message):
    """Вызвать меню смены языка"""
    await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


@dp.message_handler(commands=["country"])
async def command_country(message: types.Message):
    """Вызвать меню смены страны"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'country_choice_{user_language}'], reply_markup=country_buttons)


@dp.message_handler(commands=["chat"])
async def command_chat(message: types.Message):
    """Ссылка на чат"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'link_to_chat_{user_language}'])


@dp.message_handler(commands=["error"])
async def command_error(message: types.Message):
    """Ссылка на обсуждение ошибок"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'link_error_chat_{user_language}'])


@dp.message_handler(commands=["penalty"])
async def command_penalty(message: types.Message):
    """Раздел со штрафами. Показывает все штрафы по категориям"""
    telegram_id = message.from_user.id
    user = get_user_by(telegram_id)
    language = user.language
    country = user.country
    if country == 'RU':
        data = get_data_from_json_file('backup/penalty_russia.json')
        await message.answer(data['title'], reply_markup=russian_penalty_titles)
    else:
        data = get_data_from_json_file(f'backup/penalty_kazakhstan_{language}.json')
        if language == 'RU':
            await message.answer(data['title'], reply_markup=penalty_buttons_ru_1)
        if language == 'KZ':
            await message.answer(data['title'], reply_markup=penalty_buttons_kz_1)


@dp.message_handler(commands=["statistics"])
async def command_statistics(message: types.Message):
    """Показать статистику по пользователям, промо-кодам"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_big_statistics()
        await message.answer(result)


# переделать, отдельная команда для Ру пользователей, отдельная для КЗ
@dp.message_handler(commands=["send_post_ru", "send_post_kz", "send_post_russia", "send_post_kazakhstan"], state='*')
async def command_send_post(message: types.Message, state: FSMContext):
    """Отправить рекламное сообщение всем пользователям - фото+подпись"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer('Отправь рекламное фото и сообщение, оно будет перенаправлено всем пользователям!')
        await AllStates.SendPromotionalPost.set()
        await state.update_data(location=message.text)


@dp.message_handler(state=AllStates.SendPromotionalPost, content_types=['text', 'photo'])
async def command_send_post_action(message: types.Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    caption = message.caption
    await state.update_data(photo_id=photo_id)
    data = await state.get_data()
    comm = data['location']
    await state.finish()
    users_language, user_country = filter_telegram_id(comm)
    users = get_all_users_telegram_id(language=users_language, country=user_country)
    no_active_users = 0
    for user_id in loading_bar(users):
        try:
            await bot.send_photo(user_id, photo_id, caption=caption)
        except (ChatNotFound, UserDeactivated, BotBlocked):
            no_active_users += 1
        except Exception as exx:
            await bot.send_message(config.ADMIN_ID, str(exx))
    await bot.send_message(config.ADMIN_ID, f'Сообщение доставлено до {len(users) - no_active_users} пользователей ✌🏻\n'
                                            f'Не доставлено до {no_active_users}\n'
                                            f'Всего {len(users)} пользователей')


@dp.message_handler(commands=["promo_code"], state='*')
async def command_promo_code(message: types.Message):
    """
    Раздел с Промо-кодами. Тут можно активировать промокод и получить +3 дня к использованию бота и
    скидку 50% на покупку годового доступа
    """
    telegram_id = message.from_user.id
    user = get_user_by(telegram_id)
    language = user.language
    user_promo_code_used_status = user.promo_code_used
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
    promo_codes = get_all_promo_codes()
    if user_promo_code in promo_codes:
        up_user_time_limit_days(telegram_id, 5)
        up_number_of_references(user_promo_code)
        update_user_promo_code_used_status(telegram_id)
        commit_use_promo_code(telegram_id, user_promo_code)
        change_price_in_rubles_on_user(telegram_id, config.PRICE_AFTER_20DAYS)
        await message.answer_sticker(STICKERS['all_good'])
        await message.answer(PROMO_CODE[f'promo_code_activated_{language}'])
    else:
        await message.answer_sticker(STICKERS['NO'])
        await message.answer(PROMO_CODE[f'promo_code_error_{language}'])
    await state.finish()


@dp.message_handler(commands=["pay"])
async def command_pay(message: types.Message):
    """
    Раздел Оплаты.
    Команда pay посылает запрос в платежную систему, получает в ответ платежную ссылку и передает эту ссылку на оплату
    клиенту
    """
    telegram_id = message.from_user.id
    user = get_user_by(telegram_id)
    pay_data = PayData(user.country, user.language, user.price_in_rubles)
    pay_link = PayLinkIoka(telegram_id=telegram_id, price=pay_data.price_tenge, currency=pay_data.code,
                           name=user.full_name)
    url = pay_link.get_pay_url()

    markup = types.InlineKeyboardMarkup()
    pay_button = BUTTONS[f'pay_{user.language}']
    pay_link = types.InlineKeyboardButton(text=pay_button, url=url)
    markup.add(pay_link)

    await message.answer(pay_data.message_text, reply_markup=markup)

    await send_pay_access_message(telegram_id, user.language, 20)


async def send_pay_access_message(telegram_id: int, user_language: str, time_limit: int) -> None:
    """
    Отправить сообщение, если платеж произведен успешно
    Проверка осуществляется каждую минуту в течении ограниченного количества времени (time_limit)
    :param user_language: язык пользователя
    :param time_limit: количество минут, в течении которых ссылка активна для оплаты
    :param telegram_id: id плательщика
    """
    time_stop = datetime.now() + timedelta(minutes=time_limit)
    while True:
        await asyncio.sleep(10)
        time_now = datetime.now()
        status = await check_pay_status(telegram_id, user_language)
        if status or time_now > time_stop:
            break


async def check_pay_status(telegram_id: int, user_language: str) -> bool:
    """
    Проверить статус платежа
    :param user_language: язык пользователя
    :param telegram_id: id плательщика
    :return: True если есть номер платежа
    """
    pay_order = check_pay_order(telegram_id)
    if pay_order is not None:
        if pay_order[-1].date.date() == datetime.now().date():
            text = MESSAGE.get(f'pay_registered_message_{user_language}').format(pay_order[-1].order_number)
            await bot.send_message(telegram_id, text)
            return True


@dp.message_handler(commands=["promotions"])
async def command_promotions(message: types.Message):
    """Раздел с акциями и скидками. Пока только 1 акция с рефералкой"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    image_code = IMAGES['100friends']

    markup = types.InlineKeyboardMarkup()
    button_text = BUTTONS[f'do_it_{user_language}']
    ref_link = types.InlineKeyboardButton(text=button_text,
                                          callback_data=referral_button_call.new(referral='100friends',
                                                                                 value=user_language))
    markup.add(ref_link)

    if not config.DEBUG:
        await bot.send_photo(telegram_id, image_code)
    await message.answer(PROMOTIONS[f'100friends_{user_language}'], reply_markup=markup)


@dp.message_handler(commands=["info"])
async def command_help(message: types.Message):
    """Раздел Инфо о боте"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer_sticker(STICKERS['message'])
    await message.answer(MESSAGE[f'info_{user_language}'])
    if telegram_id == config.ADMIN_ID:
        await message.answer(MESSAGE['start_admin_text'])


@dp.message_handler(commands=["up_admin_time_limit"])
async def command_up_admin_q_a(message: types.Message):
    """Добавить 3 минуты к времени использования админу, для тестов"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        up_admin_time_limit_3minute()
        await message.answer('+3 минуты добавлено')


@dp.message_handler(commands=["up_time_limit_for_all_at_days_03", "up_time_limit_for_all_at_days_30"])
async def command_up_time_limit_for_all_at_n_day(message: types.Message):
    """
    Добавить +n дня пользования ботом всем пользователям.
    Акция на праздник или компенсация за ремонт
    """
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        days = int(message.text[-2:])
        up_all_user_time_limit(days=days)
        await message.answer(f'+{days} дней использования всем пользователям АКТИВИРОВАНО!')


@dp.message_handler(commands=["set_50_percent_price_for_losers"])
async def command_set_50_percent_price_for_losers(message: types.Message):
    """Сделать 50% скидку на покупку годового доступа для лузеров и отправить соответствующий пост"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        losers = get_losers()
        set_50_percent_price_for_losers()
        no_active_users = 0
        for user in loading_bar(losers):
            try:
                await bot.send_photo(user['telegram_id'],
                                     IMAGES['50percent'],
                                     caption=OFFERS[f'second_week_promotional_offer_{user["language"]}'])
            except (ChatNotFound, UserDeactivated, BotBlocked):
                no_active_users += 1
            except Exception as exx:
                await bot.send_message(config.ADMIN_ID, str(exx))
        await bot.send_message(config.ADMIN_ID, '50% скидка установлена ✌🏻\n'
                                                f'Оповещены {len(losers) - no_active_users} из {len(losers)}')


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    """Отправляем новый вопрос в ответ на отвеченный вопрос"""
    telegram_id = quiz_answer.user.id
    user_language = get_user_language(telegram_id)
    if not user_time_limit_is_over(telegram_id):
        question = get_random_question(user_language)
        if config.DEBUG is False and question.image_code:
            await bot.send_photo(telegram_id, question.image_code)
        options = pickle.loads(question.all_answers)
        random.shuffle(options)
        correct_option_id = options.index(question.correct_answer)
        await quiz_answer.bot.send_poll(telegram_id,
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


# АВТОШКОЛЫ -----------------------------------------------------------------------------------------------------------


@dp.message_handler(commands=["send_hello_emails_to_new_schools"])
async def command_send_hello_emails_to_new_schools(message: types.Message):
    """Отправить приветственное email сообщение новым автошколам"""
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


@dp.message_handler(commands=["send_email_for_all_auto_schools"], state='*')
async def command_send_email_for_all_auto_schools(message: types.Message):
    """Отправить email сообщение всем автошколам об изменениях в работе бота или политики"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Пиши текст.\n'
                             'Сообщение будет встроенно в HTML код и будет отправлено всем Автошколам!')
        await AllStates.SendEmailToAllAutoSchools.set()


@dp.message_handler(state=AllStates.SendEmailToAllAutoSchools, content_types=types.ContentTypes.TEXT)
async def command_send_email_for_all_auto_schools_action(message: types.Message, state: FSMContext):
    my_message = message.text
    await state.update_data(my_message=my_message)
    auto_schools = get_all_auto_schools_on_db()
    emails = get_auto_schools_emails(auto_schools)
    message_subtitle = 'Произошли изменения'
    html = new_func_and_offers_message(my_message)
    send_emails_to_schools(emails, message_subtitle, html)
    await message.answer('Сообщения о изменениях были отправлены автошколам! ✅')
    await state.finish()


@dp.message_handler(commands=["delete_auto_school"], state='*')
async def command_delete_auto_school(message: types.Message):
    """Удалить Автошколу по запросу"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        await message.answer('Напиши секретный ключ автошколы:')
        await AllStates.DeleteAutoSchool.set()


@dp.message_handler(state=AllStates.DeleteAutoSchool, content_types=types.ContentTypes.TEXT)
async def command_delete_auto_school_action(message: types.Message, state: FSMContext):
    secret_key = message.text
    await state.update_data(secret_key=secret_key)
    delete_auto_school_by(secret_key)
    await message.answer('Автошкола успешно удалена из базы!')
    await state.finish()


# ОСТАЛЬНОЕ -----------------------------------------------------------------------------------------------------------


# добавить парсер и валидацию от Pydantic
@dp.message_handler(content_types=['document'])
async def scan_message(message: types.Message):
    """Принимает JSON файл, распарсивает его и добавляем информацию об автошколах в базу"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        document_id = message.document.file_id
        file_address = await bot.download_file_by_id(document_id)
        file_data = json.load(io.TextIOWrapper(file_address, encoding='utf-8'))
        file_data = parse_schools_from_object(file_data)
        try:
            add_new_auto_schools(file_data)
            await message.answer('Информация об автошколах была добавлена в базу...')
        except KeyError as err:
            await message.answer('Не корректный набор данных!\n{}'.format(err))


@dp.message_handler(content_types=['photo'])
async def scan_photo(message: types.Message):
    """Получить id фотографии, для админа"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        photo_id = message.photo[0].file_id
        await message.answer(photo_id)


@dp.message_handler(commands=["backup_all_data"])
async def command_backup_all_data(message: types.Message):
    """Бэкап данных(пользователи и школы) и отправка админу в виде файлов JSON"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        backup_users()
        backup_auto_schools()
        path_1 = path_to_users_backup()
        path_2 = path_to_auto_schools_backup()
        with open(path_1, 'rb') as users_json_file:
            await message.answer_document(users_json_file)
        with open(path_2, 'rb') as auto_schools_json_file:
            await message.answer_document(auto_schools_json_file)


@dp.message_handler(commands=["get_user_info"])
async def command_get_user_info(message: types.Message):
    """Показать всю информацию о пользователе"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer('Напиши или пришли сообщение от пользователя')
        await AllStates.InfoAboutUser.set()


@dp.message_handler(state=AllStates.InfoAboutUser, content_types=types.ContentTypes.TEXT)
async def command_get_user_info_action(message: types.Message, state: FSMContext):
    try:
        user_info = f'ID: {message.forward_from.id}\n' \
                    f'Имя: {message.forward_from.full_name}\n' \
                    f'Ник: @{message.forward_from.username}'
    except AttributeError:
        await message.answer(GIFT_CERTIFICATE['identification_error_RU'])
    else:
        await message.answer(user_info)
    finally:
        await state.finish()


@dp.message_handler(commands=["donate"])
async def command_donate(message: types.Message):
    """Пожертвования на развитие проекта + карта развития проекта"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    image_code = IMAGES['roadmap']

    markup = types.InlineKeyboardMarkup()
    button_text = BUTTONS[f'help_project_{user_language}']
    ref_link = types.InlineKeyboardButton(text=button_text, url=config.DONATE_URL)
    markup.add(ref_link)

    if not config.DEBUG:
        await bot.send_photo(telegram_id, image_code)
    await message.answer(ROADMAP[f'roadmap_text_{user_language}'], reply_markup=markup)


@dp.message_handler(commands=["certificate"])
async def command_certificate(message: types.Message):
    """Подарочный сертификат на покупку тарифа Премиум Max"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE.get(f'function_error_{user_language}'))


@dp.message_handler()
async def simple_message(message: types.Message):
    """Показать меню"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    commands = COMMANDS_DESCRIPTIONS.get(user_language, 'ALL')
    text = [f"/{key} - {value}" for (key, value) in commands.items() if key != 'language_code']
    await message.answer("\n".join(text))


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
