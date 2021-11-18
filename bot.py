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
from keyboards.cancel import get_cancel_button
from keyboards.inline.question import get_question_button
from keyboards.inline.button_with_url import get_url_button
import messages
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
    PollAnswers: State = State()


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
    """
    Начало работы. Приветственное сообщение
    Добавление бонусов пригласившего реферала
    Вызов меню регистрации пользователя
    """
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    referral_telegram_id = message.get_args()
    question_button = ''

    # запихнуть в функцию?
    user = get_user_by(telegram_id)
    invited_user = search_user_in_gifts(telegram_id)
    if user:
        if user.leaver:
            edit_leaver_status(telegram_id, False)
            question_button = get_question_button(user.language)
    elif invited_user:
        add_user(telegram_id, full_name, referral_id=invited_user.referral_id, tariff='premium_max')
        up_user_referral_bonus(referral_telegram_id)
        await send_message_about_successful_attracting(referral_telegram_id)
    else:
        add_user(telegram_id, full_name, referral_id=referral_telegram_id)
        up_user_referral_bonus(referral_telegram_id)
        await send_message_about_successful_attracting(referral_telegram_id)

    await bot.send_sticker(telegram_id, messages.STICKERS['hello'])
    await message.answer(MESSAGE['start_user_text'].format(full_name), reply_markup=question_button)
    if not get_user_registration_status(telegram_id):
        await message.answer(MESSAGE['language_choice'], reply_markup=language_buttons)


async def send_message_about_successful_attracting(telegram_id: Union[str, int]) -> None:
    """
    Сообщение рефералу об увеличении дневного лимита
    :param telegram_id: id
    :return:
    """
    user = get_user_by(telegram_id)
    if not user.leaver:
        text = MESSAGE.get(f'attraction_text_{user.language}')
        try:
            await bot.send_message(telegram_id, text)
        except (ChatNotFound, UserDeactivated, BotBlocked):
            edit_leaver_status(telegram_id, True)
        except Exception as exx:
            await bot.send_message(config.ADMIN_ID, str(exx))


@dp.message_handler(commands=["question"])
async def command_question(message: types.Message):
    """Отправить случайный вопрос из базы"""
    telegram_id = message.from_user.id
    await send_quiz(telegram_id)


# возможно нужно делать через состояния. id ответа из quiz_answer.option_ids а правильный id из состояния
@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    """В ответ на викторину, отправляем новую викторину"""
    telegram_id = quiz_answer.user.id
    await send_quiz(telegram_id)


async def send_quiz(telegram_id):
    user_language = get_user_language(telegram_id)
    if get_user_daily_limit(telegram_id) > 0:
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
        update_user_daily_limit(telegram_id, -1)
    else:
        await bot.send_sticker(telegram_id, messages.STICKERS['flower'])
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
    """Ссылка на чат (форум)"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'link_to_chat_{user_language}'])


@dp.message_handler(commands=["error"])
async def command_error(message: types.Message):
    """Ссылка на чат обсуждения ошибок"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE[f'link_error_chat_{user_language}'])


@dp.message_handler(commands=["penalty"])
async def command_penalty(message: types.Message):
    """Раздел со штрафами. Показывает размеры всех штрафов по категориям"""
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
    """Показать статистику по пользователям, промо-кодам, автошколам"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        result = get_big_statistics()
        await message.answer(result)


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
    for user_id in loading_bar(users):
        try:
            await bot.send_photo(user_id, photo_id, caption=caption)
        except (ChatNotFound, UserDeactivated, BotBlocked):
            edit_leaver_status(user_id, True)
        except Exception as exx:
            await bot.send_message(config.ADMIN_ID, str(exx))
    await bot.send_message(config.ADMIN_ID, f'Сообщение доставлено до {len(users)} пользователей ✌🏻\n')


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
        await message.answer(messages.PROMO_CODE[f'promo_code_command_text_{language}'],
                             reply_markup=get_cancel_button(language))
        await AllStates.UsePromoCode.set()
    else:
        await message.answer_sticker(messages.STICKERS['NO'])
        await message.answer(messages.PROMO_CODE[f'promo_code_was_used_{language}'])


@dp.message_handler(state=AllStates.UsePromoCode, content_types=types.ContentTypes.TEXT)
async def command_promo_code_action(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    language = get_user_language(telegram_id)
    user_promo_code = message.text
    if user_promo_code == messages.BUTTONS[f'cancel_{language}']:
        await message.answer(MESSAGE[f'cancel_action_{language}'], reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        user_promo_code = message.text.upper()
        await state.update_data(user_promo_code=user_promo_code)
        promo_codes = get_all_promo_codes()
        if user_promo_code in promo_codes:
            up_user_time_limit_days(telegram_id, 5)
            up_number_of_references(user_promo_code)
            update_user_promo_code_used_status(telegram_id)
            commit_use_promo_code(telegram_id, user_promo_code)
            change_price_in_rubles_on_user(telegram_id, config.PRICE_AFTER_20DAYS)
            await message.answer_sticker(messages.STICKERS['all_good'], reply_markup=types.ReplyKeyboardRemove())
            await message.answer(messages.PROMO_CODE[f'promo_code_activated_{language}'],
                                 reply_markup=get_question_button(language))
            await state.finish()
        else:
            await message.answer_sticker(messages.STICKERS['NO'])
            await message.answer(messages.PROMO_CODE[f'promo_code_error_{language}'])


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

    link_button = get_url_button(messages.BUTTONS[f'pay_{user.language}'], pay_link.get_pay_url())
    await message.answer(pay_data.message_text, reply_markup=link_button)
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
            await bot.send_message(telegram_id, text, reply_markup=get_question_button(user_language))
            return True


@dp.message_handler(commands=["promotions"])
async def command_promotions(message: types.Message):
    """Раздел с акциями и скидками. Пока только 1 акция с рефералкой"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    image_code = messages.IMAGES['100friends']

    markup = types.InlineKeyboardMarkup()
    button_text = messages.BUTTONS[f'do_it_{user_language}']
    ref_link = types.InlineKeyboardButton(text=button_text,
                                          callback_data=referral_button_call.new(referral='100friends',
                                                                                 value=user_language))
    markup.add(ref_link)

    if not config.DEBUG:
        await bot.send_photo(telegram_id, image_code)
    await message.answer(messages.PROMOTIONS[f'100friends_{user_language}'], reply_markup=markup)


@dp.message_handler(commands=["info"])
async def command_help(message: types.Message):
    """Раздел Инфо о боте"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer_sticker(messages.STICKERS['message'])
    await message.answer(MESSAGE[f'info_{user_language}'])
    if telegram_id == config.ADMIN_ID:
        await message.answer(messages.ADMIN_MENU_TEXT)


# переделать в 50% скидку для всех на праздники
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
                                     messages.IMAGES['50percent'],
                                     caption=messages.OFFERS[f'second_week_promotional_offer_{user["language"]}'])
            except (ChatNotFound, UserDeactivated, BotBlocked):
                no_active_users += 1
            except Exception as exx:
                await bot.send_message(config.ADMIN_ID, str(exx))
        await bot.send_message(config.ADMIN_ID, '50% скидка установлена ✌🏻\n'
                                                f'Оповещены {len(losers) - no_active_users} из {len(losers)}')


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


# ОСТАЛЬНОЕ -----------------------------------------------------------------------------------------------------------


@dp.message_handler(content_types=['photo'])
async def scan_photo(message: types.Message):
    """Получить id фотографии, для админа"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        photo_id = message.photo[0].file_id
        await message.answer(photo_id)


@dp.message_handler(commands=["donate"])
async def command_donate(message: types.Message):
    """Пожертвования на развитие проекта + карта развития проекта"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)

    image_code = messages.IMAGES[f'roadmap_{user_language}']
    if not config.DEBUG:
        await bot.send_photo(telegram_id, image_code)

    link_button = get_url_button(text=messages.BUTTONS[f'help_project_{user_language}'], url=config.DONATE_URL)
    await message.answer(messages.ROADMAP[f'roadmap_text_{user_language}'], reply_markup=link_button)


@dp.message_handler(commands=["certificate"])
async def command_certificate(message: types.Message):
    """Подарочный сертификат на покупку тарифа Премиум Max"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    await message.answer(MESSAGE.get(f'function_error_{user_language}'))


# АДМИНКА -------------------------------------------------------------------------------------------------------------


@dp.message_handler(commands=["up_admin_daily_limit"])
async def command_up_admin_daily_limit(message: types.Message):
    """Добавить 5 вопросов админу, для тестов"""
    user_id = message.from_user.id
    if user_id == config.ADMIN_ID:
        up_admin_daily_limit()
        await message.answer('Добавлено 5 вопросов к дневному лимиту')


@dp.message_handler(commands=["get_user_info"])
async def command_get_user_info(message: types.Message):
    """Показать всю информацию о пользователе"""
    telegram_id = message.from_user.id
    if telegram_id == config.ADMIN_ID:
        await message.answer('Напиши или пришли сообщение от пользователя')
        await AllStates.InfoAboutUser.set()


@dp.message_handler(state=AllStates.InfoAboutUser, content_types=types.ContentTypes.TEXT)
async def command_get_user_info_action(message: types.Message, state: FSMContext):
    user_info = 'ID: {}\n' \
                'Имя: {}\n' \
                'Ник: @{}'
    try:
        user_id = message.forward_from.id
        full_name = message.forward_from.full_name
        username = message.forward_from.username
        user_info = user_info.format(user_id, full_name, username)
    except AttributeError:
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        username = message.from_user.username
        user_info = user_info.format(user_id, full_name, username)
        await message.answer(messages.GIFT_CERTIFICATE['identification_error_RU'])
        await message.answer(user_info)
    else:
        await message.answer(user_info)
    finally:
        await state.finish()


# ДОЛЖНО БЫТЬ ВСЕГДА В КОНЦЕ КОДА, НЕ ПЕРЕМЕЩАТЬ! ---------------------------------------------------------------------


@dp.message_handler()
async def simple_message(message: types.Message):
    """Показать меню"""
    telegram_id = message.from_user.id
    user_language = get_user_language(telegram_id)
    commands = COMMANDS_DESCRIPTIONS.get(user_language, COMMANDS_DESCRIPTIONS['ALL'])
    text = [f"/{key} - {value}" for (key, value) in commands.items() if key != 'language_code']
    await message.answer("\n".join(text))


if __name__ == "__main__":
    from handlers import dp

    executor.start_polling(dp, skip_updates=True)
