import json
import random
import string
from db_models import *
from datetime import datetime, timedelta
import config
import pickle
from google_trans_new import google_translator
from google_trans_new.google_trans_new import google_new_transError
from messages import COMMANDS_DESCRIPTIONS, PAY
from typing import List, Union


# КАРТИНКИ -----------------------------------------------------------------------------------------------------------


def get_image_codes_from(txt_file_name):
    with open(txt_file_name, encoding='utf-8-sig', mode='r') as f:
        text = f.readlines()
    new_list = [el.replace('\n', '') for el in text]
    return new_list


def add_image_code_to(db_name, image_code_list):
    for question in db_name:
        question['image_code'] = image_code_list.pop(0)
    return db_name


def edit_image_code(old_code, new_code):
    QuestionRU.update(image_code=new_code).where(QuestionRU.image_code == old_code).execute()
    QuestionKZ.update(image_code=new_code).where(QuestionKZ.image_code == old_code).execute()


# ПЕРЕВОД ------------------------------------------------------------------------------------------------------------


translator = google_translator(timeout=30)


def translate_to_kz(text):
    translated_text = translator.translate(text, lang_src='ru', lang_tgt='kk')
    return translated_text


def translate_list_to_kz(questions_list):
    translated_list = list(map(lambda x: translator.translate(x, lang_src='ru', lang_tgt='kk').strip(), questions_list))
    return translated_list


def translate_dict_to_kz_language(ru_question):
    try:
        question = translate_to_kz(ru_question['question']).strip()
        all_answers = translate_list_to_kz(ru_question['all_answers'])
        correct_answer = translate_to_kz(ru_question['correct_answer']).strip()
        explanation = translate_to_kz(ru_question['explanation']).strip()
        image_code = ru_question['image_code']
        kz_question = {'question': question, 'all_answers': all_answers, 'correct_answer': correct_answer,
                       'image_code': image_code, 'explanation': explanation}
        return kz_question
    except google_new_transError:
        return False


def translate_penalty_to_kz_language(ru_penalty):
    try:
        small_title = translate_to_kz(ru_penalty['small_title']).strip()
        title = translate_to_kz(ru_penalty['title']).strip()
        answers = translate_list_to_kz(ru_penalty['answers'])
        description = translate_to_kz(ru_penalty['description']).strip()
        kz_penalty = {'small_title': small_title, 'title': title, 'answers': answers, 'description': description}
        return kz_penalty
    except google_new_transError:
        return False


def translate_penalty_to_kz(penalty):
    all_penalty = []
    for el in penalty:
        data = translate_penalty_to_kz_language(el)
        all_penalty.append(data)
    return all_penalty


def beautiful_print_data_from_db(db_name):
    print(json.dumps(db_name, sort_keys=True, indent=4, ensure_ascii=False))


def beautiful_print_data_from_dict(dict_name):
    for el in dict_name:
        print(el, end=',\n')


def get_data_from_json_file(json_file_name):
    try:
        with open(json_file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return False


def edit_data_in_json_file(json_file_name, new_data):
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(new_data, json_file, ensure_ascii=False)


def create_new_json_file(json_file_name, questions_list):
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(questions_list, json_file, ensure_ascii=False, default=str)


def create_null_json_file(json_file_name):
    null_list = []
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(null_list, json_file, ensure_ascii=False)


def translate_db_to_kz_language(db_name, json_file_name):
    data = get_data_from_json_file(json_file_name)
    if not data:
        data = ''
        create_null_json_file(json_file_name)

    for ru_question in db_name[len(data):]:
        kz_question = translate_dict_to_kz_language(ru_question)
        if not kz_question:
            print('Limit error')
            return

        data = get_data_from_json_file(json_file_name)
        data.append(kz_question)
        edit_data_in_json_file(json_file_name, data)

    print('Yippee! Translation finished!!!')


# ВОПРОСЫ ------------------------------------------------------------------------------------------------------------


def new_ru_question(question, correct_answer, all_answers, explanation=None, image_code=None):
    database_initialization()
    new_question = QuestionRU(question=question,
                              correct_answer=correct_answer,
                              all_answers=all_answers,
                              explanation=explanation,
                              image_code=image_code
                              )
    new_question.save()


def new_kz_question(question, correct_answer, all_answers, explanation=None, image_code=None):
    database_initialization()
    new_question = QuestionKZ(question=question,
                              correct_answer=correct_answer,
                              all_answers=all_answers,
                              explanation=explanation,
                              image_code=image_code
                              )
    new_question.save()


def get_number_of_questions_in_db_and_set_in_cache(database, user_language):
    count = len(database.select())
    config.CACHE[f'number_of_questions_in_{user_language}_db'] = count
    return count


def questions_to_db(raw_db, language):
    database_initialization()
    for el in raw_db:
        question = el['question']
        correct_answer = el['correct_answer']
        all_answers = pickle.dumps(el['all_answers'], pickle.HIGHEST_PROTOCOL)
        explanation = el['explanation']
        image_code = el['image_code']
        if language == 'KZ':
            new_kz_question(question, correct_answer, all_answers, explanation, image_code)
        else:
            new_ru_question(question, correct_answer, all_answers, explanation, image_code)


def write_all_questions_in_db(json_file_name, language):
    data = get_data_from_json_file(json_file_name)
    questions_to_db(data, language)
    print(f'Вопросы добавлены в таблицу {language}...\n'
          f'Не забудь закомментировать эту строку кода!')


def choose_db_by_language(user_language):
    if user_language == 'RU':
        return QuestionRU
    elif user_language == 'KZ':
        return QuestionKZ


def get_random_question(user_language):
    database_initialization()
    database = choose_db_by_language(user_language)
    number_of_questions = config.CACHE.get(
        f'number_of_questions_in_{user_language}_db') or get_number_of_questions_in_db_and_set_in_cache(database,
                                                                                                        user_language)
    random_id = random.randrange(1, number_of_questions + 1)
    question = database.get(database.id == random_id)
    return question


def get_all_questions_from_db(user_language):
    db_name = choose_db_by_language(user_language)
    database_initialization()
    questions = db_name.select()
    questions_list = []
    for el in questions:
        question_id = el.id
        question = el.question
        correct_answer = el.correct_answer
        all_answers = pickle.loads(el.all_answers)
        explanation = el.explanation
        image_code = el.image_code
        question_dict = {'id': question_id, 'question': question, 'correct_answer': correct_answer,
                         'all_answers': all_answers, 'explanation': explanation, 'image_code': image_code}
        questions_list.append(question_dict)
    return questions_list


# ПОЛЬЗОВАТЕЛЬ -------------------------------------------------------------------------------------------------------


# price_in_rubles удалить
def add_user(telegram_id: int, full_name: str, referral_id: int = None, tariff: str = 'basic') -> None:
    """Добавить нового пользователя в базу, таблица users"""
    database_initialization()
    daily_limit = config.TARIFFS[tariff]['daily_limit']
    try:
        User(telegram_id=telegram_id, full_name=full_name, price_in_rubles=300, referral_id=referral_id,
             tariff=tariff, daily_limit=daily_limit).save()
    except IntegrityError as err:
        print(err)
        assert err


def delete_user(telegram_id: int) -> None:
    """Удалить пользователя из таблицы users"""
    database_initialization()
    try:
        User.delete().where(User.telegram_id == telegram_id).execute()
    except Exception as err:
        print(err)
        assert err


def change_tariff(telegram_id: int, new_tariff: str) -> None:
    """
    Изменить тариф пользователя
    :param telegram_id: id
    :param new_tariff: название тарифа
    :return:
    """
    edit_user_tariff(telegram_id, new_tariff)
    update_user_daily_limit(telegram_id, config.TARIFFS[new_tariff]['daily_limit'])


def edit_user_tariff(telegram_id: int, new_tariff: str) -> None:
    """
    Изменить тариф пользователя
    :param telegram_id: id
    :param new_tariff: название тарифа
    :return:
    """
    User.update(tariff=new_tariff).where(User.telegram_id == telegram_id).execute()


def update_user_daily_limit(telegram_id, count: int):
    """
    Получить доступный дневной лимит вопросов пользователя
    :param telegram_id: id
    :param count: число, на которое стоит увеличить или уменьшить дневной лимит +/- number
    :return:
    """
    database_initialization()
    User.update(daily_limit=User.daily_limit + count).where(User.telegram_id == telegram_id).execute()


def search_user_in_gifts(telegram_id: int) -> Union[Gift, None]:
    """
    Проверить наличие id пользователя в купленных подарочных сертификатах
    :param telegram_id: id
    :return: запись о подарочном сертификате / None
    """
    database_initialization()
    try:
        gift = Gift.get(Gift.telegram_id == telegram_id)
    except Exception as exx:
        print(exx)
    else:
        return gift

# переписать
# def set_user_on_db(telegram_id, full_name, country, language, registration_date, registration_is_over,
#                last_visit, discount, made_payment, second_week_promotional_offer,
#                sixth_week_promotional_offer):
# """Это когда добавляешь пользователя из JSON файла в базу (гавнокод), нужно будет переписать.
# Спарсить всех пользователей из JSON файла модулем Pydantic и передавать сюда 1 параметр типа object"""
# registration_date = convert_str_to_datetime(registration_date)
# time_limit = convert_str_to_datetime(time_limit)
# last_visit = convert_str_to_datetime(last_visit)
# try:
#     database_initialization()
#     user = User(telegram_id=telegram_id,
#                 full_name=full_name,
#                 country=country,
#                 language=language,
#                 registration_date=registration_date,
#                 registration_is_over=registration_is_over,
#                 time_limit=time_limit,
#                 last_visit=last_visit,
#                 promo_code_used=promo_code_used,
#                 price_in_rubles=price_in_rubles,
#                 made_payment=made_payment,
#                 second_week_promotional_offer=second_week_promotional_offer,
#                 sixth_week_promotional_offer=sixth_week_promotional_offer)
#     user.save()
# except IntegrityError:
#     pass


def valid_id(telegram_id):
    if str(telegram_id).isdigit():
        return True


def get_user_by(telegram_id) -> User:
    """
    Получить пользователя по telegram_id
    :param telegram_id: id
    :return: объект класса User
    """
    database_initialization()
    try:
        user = User.get(User.telegram_id == telegram_id)
    except Exception as exx:
        print(exx)
    else:
        return user


def get_all_users_in_db() -> User:
    """
    Получить всех пользователей из базы данных (для статистики)
    :return: Данные о всех пользователях из базы
    """
    database_initialization()
    users = User.select()
    return users


def get_user_name_by(telegram_id):
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    return user.full_name


def get_user_language(telegram_id):
    """Получить язык пользователя из кэша/базы"""
    user_language = config.users_data_cache.get(telegram_id)
    if user_language:
        return user_language
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    config.users_data_cache[telegram_id] = user.language
    return user.language


def edit_user_language(telegram_id: int, new_user_language) -> None:
    """
    :param telegram_id: telegram_id
    :param new_user_language: 'RU' or 'KZ'
    """
    database_initialization()
    User.update(language=new_user_language).where(User.telegram_id == telegram_id).execute()
    config.users_data_cache[telegram_id] = new_user_language


def get_user_country(telegram_id: int) -> str:
    """Получить страну пользователя из базы"""
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    return user.country


def edit_user_country(telegram_id, user_country) -> None:
    """Изменить страну пользователя"""
    database_initialization()
    User.update(country=user_country).where(User.telegram_id == telegram_id).execute()


def edit_leaver_status(telegram_id: int, status: bool) -> None:
    """
    :param telegram_id: telegram_id
    :param status: True / False
    """
    database_initialization()
    User.update(leaver=status).where(User.telegram_id == telegram_id).execute()


class PayData:
    def __init__(self, obj: User, purchased_tariff):
        """
        Высчитывает финальную стоимость тарифа и формирует текст описания
        Прием оплаты в рублях не работает (платежная система IOKA)
        (398 - код тенге, 643 - код рубля)
        :param obj: Пользователь
        """
        self.purchased_tariff = purchased_tariff
        self.tariff_translate = config.TARIFFS[purchased_tariff]['translate']
        self.user_country = obj.country
        self.user_language = obj.language
        self.code = 398
        self.event = 2 if config.EVENT else 1
        self.discount = 2 if obj.discount else 1
        self.price_ruble = int(config.TARIFFS[purchased_tariff]['price'] / self.event / self.discount)
        self.price_tenge = int(self.price_ruble * config.RUBLES_EXCHANGE_RATE)
        self.message_text = PAY[f'message_{self.user_country}_{self.user_language}'].format(
            tariff=self.tariff_translate, price_ruble=self.price_ruble, price_tenge=self.price_tenge)


def get_user_time_limit(telegram_id):
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    date_time = user.time_limit
    return date_time


def user_time_limit_is_over(telegram_id):
    today = datetime.now()
    database_initialization()
    time_limit = get_user_time_limit(telegram_id)
    if time_limit < today:
        return True
    else:
        return False


def get_user_daily_limit(telegram_id) -> int:
    """
    Получить доступный дневной лимит вопросов пользователя
    :param telegram_id: id
    :return: лимит вопросов
    """
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    daily_limit = user.daily_limit
    return daily_limit


def up_admin_daily_limit() -> None:
    """
    Увеличить дневной лимит админу
    :return:
    """
    database_initialization()
    User.update(daily_limit=User.daily_limit + 5).where(User.telegram_id == config.ADMIN_ID).execute()


def up_user_daily_limit(telegram_id: Union[int, str], count: int = 5) -> None:
    """
    Увеличить число дневного лимита (единоразово, при подключении тарифов Премиум и Премиум Мах)
    :param telegram_id: id
    :param count: число
    :return:
    """
    database_initialization()
    if valid_id(telegram_id):
        try:
            User.update(daily_limit=User.daily_limit + count).where(User.telegram_id == telegram_id).execute()
        except Exception as exx:
            print(exx)


def up_user_referral_bonus(telegram_id: Union[int, str], count: int = 1) -> None:
    """
    Увеличить число Реферального бонуса
    :param telegram_id: id
    :param count: число
    :return:
    """
    database_initialization()
    if valid_id(telegram_id):
        try:
            User.update(referral_bonus=User.referral_bonus + count).where(User.telegram_id == telegram_id).execute()
        except Exception as exx:
            print(exx)


def get_time_visit(telegram_id):
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    return user.last_visit


def get_time_limit(user: User) -> (timedelta, str):
    """
    Пользователя достопно нелимитированных 3 часа при регистрации
    :param user: Объект пользователя
    :return: количество оставшихся секунд из 10800 (3 часа) и строковое представление в час/минута
    """
    start_time = user.registration_date - datetime.now()
    sec_limit = 10800 + start_time.total_seconds()
    if sec_limit > 0:
        hours = sec_limit // 3600
        minutes = (sec_limit % 3600) / 60
        return sec_limit, '{} {} {} минут'.format(
            round(hours), 'часа' if user.language == 'RU' else 'сағат', round(minutes)
        )
    else:
        return 0, '0 часов 0 минут' if user.language == 'RU' else '0 сағат 0 минут'


def get_user_registration_status(telegram_id):
    database_initialization()
    user = User.get(User.telegram_id == telegram_id)
    return user.registration_is_over


def update_registration_status(telegram_id):
    database_initialization()
    query = User.update(registration_is_over=True).where(User.telegram_id == telegram_id)
    query.execute()


def update_user_discount_status(telegram_id):
    database_initialization()
    query = User.update(discount=True).where(User.telegram_id == telegram_id)
    query.execute()


def update_user_made_payment_status(telegram_id):
    database_initialization()
    query = User.update(made_payment=True).where(User.telegram_id == telegram_id)
    query.execute()


def update_time_visit(telegram_id):
    database_initialization()
    query = User.update(last_visit=datetime.now()).where(User.telegram_id == telegram_id)
    query.execute()


def get_all_users_telegram_id(language: str = '', country: str = '') -> tuple:
    """
    Получить telegram_id пользователей (фильтр по языку)
    :param language: Язык пользователей
    :param country: Страна пользователей
    :return: список id пользователей
    """
    database_initialization()
    if language:
        users = User.select(User.telegram_id).where((User.language == language) & (User.leaver == 0))
    elif country:
        users = User.select(User.telegram_id).where((User.country == country) & (User.leaver == 0))
    else:
        users = User.select(User.telegram_id).where(User.leaver == 0)
    telegram_ids = tuple(user.telegram_id for user in users)
    return telegram_ids


def filter_telegram_id(command: str):
    language = ''
    country = ''
    if command == '/send_post_ru':
        language = 'RU'
    elif command == '/send_post_kz':
        language = 'KZ'
    elif command == '/send_post_russia':
        country = 'RU'
    elif command == '/send_post_kazakhstan':
        country = 'KZ'
    return language, country


# def get_all_users_on_dict_format():
#     all_users_list = []
#     database_initialization()
#     all_users = User.select()
#     for user in all_users:
#         simple_user = {'id': user.id,
#                        'telegram_id': user.telegram_id,
#                        'full_name': user.full_name,
#                        'country': user.country,
#                        'language': user.language,
#                        'registration_date': user.registration_date,
#                        'registration_is_over': user.registration_is_over,
#                        'time_limit': user.time_limit,
#                        'last_visit': user.last_visit,
#                        'promo_code_used': user.promo_code_used,
#                        'price_in_rubles': user.price_in_rubles,
#                        'made_payment': user.made_payment,
#                        'second_week_promotional_offer': user.second_week_promotional_offer,
#                        'sixth_week_promotional_offer': user.sixth_week_promotional_offer}
#         all_users_list.append(simple_user)
#     return all_users_list


# ПОДАРОЧНЫЕ СЕРТИФИКАТЫ ----------------------------------------------------------------------------------------------


def get_all_gifts_telegram_id() -> tuple:
    """
    Получить telegram_id ливеров
    :return: список id пользователей
    """
    database_initialization()
    users = Gift.select(Gift.telegram_id)
    telegram_ids = tuple(user.telegram_id for user in users)
    return telegram_ids


# ПРОМО-КОДЫ и АВТОШКОЛЫ ----------------------------------------------------------------------------------------------


def commit_use_promo_code_in_base(telegram_id, promo_code):
    PromoCode(telegram_id=telegram_id, promo_code=promo_code).save()


def get_all_auto_schools_on_db():
    database_initialization()
    all_auto_schools = AutoSchool.select()
    return all_auto_schools


def get_not_notified_auto_schools_on_db():
    database_initialization()
    auto_schools = AutoSchool.select().where(AutoSchool.notified == 0)
    return auto_schools


def get_all_secret_keys():
    auto_schools = get_all_auto_schools_on_db()
    all_secret_keys = [school.secret_key for school in auto_schools]
    return all_secret_keys


def get_all_promo_codes():
    auto_schools = get_all_auto_schools_on_db()
    promo_codes_list = [school.promo_code.upper() for school in auto_schools]
    return promo_codes_list


def get_auto_schools_emails(auto_schools):
    emails = [pickle.loads(school.emails) for school in auto_schools if pickle.loads(school.emails)]
    return sum(emails, [])


def get_auto_schools_phones(auto_schools):
    phones = [pickle.loads(school.phones) for school in auto_schools if pickle.loads(school.phones)]
    return sum(phones, [])


def get_auto_schools_instagrams(auto_schools):
    instagrams = [school.instagram for school in auto_schools if school.instagram]
    return instagrams


def check_promo_code(promo_code):
    promo_codes = get_all_promo_codes()
    if promo_code in promo_codes:
        return True


def edit_promo_code(secret_key, new_promo_code):
    database_initialization()
    AutoSchool.update(promo_code=new_promo_code).where(AutoSchool.secret_key == secret_key).execute()


def edit_auto_school_by(secret_key, param, new_data):
    database_initialization()
    new_data = pickle.dumps(new_data, pickle.HIGHEST_PROTOCOL)
    if param == 'phones':
        AutoSchool.update(phones=new_data).where(AutoSchool.secret_key == secret_key).execute()
    elif param == 'emails':
        AutoSchool.update(emails=new_data).where(AutoSchool.secret_key == secret_key).execute()


def add_new_auto_schools(auto_schools) -> None:
    """
    Добавить новые автошколы в базу из документа (объекта)
    :param auto_schools: Объект со списком автошкол
    """
    for school in auto_schools:
        add_new_auto_school(school.school_name, school.country, school.city,
                            school.phones, school.emails, school.instagram)


def add_new_auto_school(school_name: str, country: str, city: str,
                        phones: list = None, emails: list = None, instagram: str = None):
    """
    Добавить новую автошколу в базу
    :param school_name: название
    :param country: страна
    :param city: город
    :param phones: список с номерами телефонов или None
    :param emails: список с адресами почты или None
    :param instagram: адрес инстаграм или None
    :return:
    """
    database_initialization()
    secret_key = get_unique_secret_key()
    try:
        AutoSchool(school_name=school_name,
                   country=country,
                   city=city,
                   phones=pickle.dumps(phones, pickle.HIGHEST_PROTOCOL),
                   emails=pickle.dumps(emails, pickle.HIGHEST_PROTOCOL),
                   instagram=instagram,
                   secret_key=secret_key,
                   promo_code=secret_key
                   ).save()
    except IntegrityError as err:
        print(err)


def add_auto_school_from_backup(auto_school) -> None:
    """Добавить автошколу в бд из бэкапа"""
    database_initialization()
    try:
        AutoSchool(school_name=auto_school.school_name,
                   country=auto_school.country,
                   city=auto_school.city,
                   phones=pickle.dumps(auto_school.phones, pickle.HIGHEST_PROTOCOL),
                   emails=pickle.dumps(auto_school.emails, pickle.HIGHEST_PROTOCOL),
                   instagram=auto_school.instagram,
                   registration_date=convert_str_to_date(auto_school.registration_date),
                   secret_key=auto_school.secret_key,
                   promo_code=auto_school.promo_code,
                   number_of_references=auto_school.number_of_references,
                   notified=auto_school.notified
                   ).save()
    except IntegrityError as err:
        print(err)


def get_auto_school_by(secret_key):
    database_initialization()
    school = AutoSchool.get(AutoSchool.secret_key == secret_key)
    return school


def get_auto_school_emails_by(secret_key):
    database_initialization()
    school = AutoSchool.get(AutoSchool.secret_key == secret_key)
    emails = pickle.loads(school.emails)
    return emails


def delete_auto_school_by(secret_key):
    database_initialization()
    AutoSchool.delete().where(AutoSchool.secret_key == secret_key).execute()


def get_not_notified_auto_schools():
    database_initialization()
    auto_schools = AutoSchool.select().where(AutoSchool.notified == 0)
    return auto_schools


# нужен?
def get_all_auto_schools_on_dict_format(auto_schools_in_db) -> List[dict]:
    """Преобразует объект в словарь"""
    all_schools = []
    for school in auto_schools_in_db:
        data = {'id': school.id,
                'school_name': school.school_name,
                'country': school.country,
                'city': school.city,
                'phones': pickle.loads(school.phones),
                'emails': pickle.loads(school.emails),
                'instagram': school.instagram,
                'registration_date': school.registration_date,
                'secret_key': school.secret_key,
                'promo_code': school.promo_code,
                'number_of_references': school.number_of_references,
                'notified': school.notified}
        all_schools.append(data)
    return all_schools


def edit_notified_status(school_id):
    database_initialization()
    AutoSchool.update(notified=True).where(AutoSchool.id == school_id).execute()


def check_secret_key(secret_key):
    secret_keys = get_all_secret_keys()
    if secret_key in secret_keys:
        return True


def get_random_secret_key():
    letters_and_digits = string.ascii_letters + string.digits
    secret_key = ''.join((random.choice(letters_and_digits) for _ in range(22)))
    return secret_key


def get_unique_secret_key():
    while True:
        secret_key = get_random_secret_key()
        if check_secret_key(secret_key):
            continue
        else:
            return secret_key


def get_number_of_references(promo_code):
    database_initialization()
    school = AutoSchool.get(AutoSchool.promo_code == promo_code)
    number_of_references = school.number_of_references
    return number_of_references


def up_auto_school_number_of_references(promo_code):
    database_initialization()
    AutoSchool.update(number_of_references=AutoSchool.number_of_references + 1).where(
        AutoSchool.promo_code == promo_code).execute()


def correct_letters_filter(promo_code):
    promo_code = promo_code.upper()
    allowed_characters = string.ascii_uppercase + string.digits + '.-_, +#№$!%&?*'
    correct_promo_code = [c for c in promo_code if c in allowed_characters]
    return ''.join(correct_promo_code)


def promo_code_check_to_correct(promo_code):
    correct_promo_code = correct_letters_filter(promo_code)
    if promo_code == correct_promo_code:
        return True


# ПЛАТЕЖИ ------------------------------------------------------------------------------------------------------------


def new_pay_order(telegram_id: int, order_number: int, price: int, tariff: str) -> None:
    """
    Добавить информацию о новом платеже в базу
    :param tariff: тариф
    :param telegram_id: id плательщика
    :param order_number: номер платежа
    :param price: цена во время оплаты (в тенге)
    """
    database_initialization()
    try:
        PayOrder(telegram_id=telegram_id, order_number=order_number, price=price, tariff=tariff).save()
    except IntegrityError:
        pass
    except Exception as exx:
        print(exx)


def check_pay_orders(telegram_id: int) -> Union[PayOrder, None]:
    """
    Получить запись о платеже, тем самым подтвердить что платеж был
    :param telegram_id: id плательщика
    :return: объект со списком платежей / None
    """
    database_initialization()
    try:
        pay_order = PayOrder.select().where(PayOrder.telegram_id == telegram_id)
    except Exception as err:
        print('Платеж не найден\n', err)
    else:
        if pay_order:
            return pay_order


# БЭКАП ДАННЫХ -------------------------------------------------------------------------------------------------------


def convert_str_to_datetime(date_time: str) -> datetime:
    date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    return date_time


def convert_str_to_date(registration_date: str) -> datetime.date:
    print(registration_date)
    date = datetime.strptime(registration_date, '%Y-%m-%d')
    return date


# СТАТИСТИКА ---------------------------------------------------------------------------------------------------------


def get_number_of_users() -> int:
    users = User.select().count()
    return users


def get_number_of_active_users() -> int:
    active_users = User.select().where(User.leaver == 0).count()
    return active_users


def get_percentage_between_active_and_liveried_users(users_count, active_users_count, leavers_count):
    active_users = round(active_users_count * 100 / users_count)
    leavers = round(leavers_count * 100 / users_count)
    return active_users, leavers


def get_number_of_leavers() -> int:
    leavers = User.select().where(User.leaver == 1).count()
    return leavers


def get_number_of_registrations_today(users):
    today = datetime.now().date()
    users = [user.id for user in users if user.registration_date.date() == today]
    return len(users)


def get_number_of_registrations_on_week(users):
    seven_day_ago = datetime.now().date() - timedelta(days=7)
    users = [user.id for user in users if user.registration_date.date() > seven_day_ago]
    return len(users)


def get_number_of_registrations_on_month(users):
    this_year = datetime.now().year
    this_month = datetime.now().month
    users = [user.id for user in users if
             user.registration_date.year == this_year and user.registration_date.month == this_month]
    return len(users)


def get_number_of_registrations_on_year(users):
    this_year = datetime.now().year
    users = [user.id for user in users if user.registration_date.year == this_year]
    return len(users)


def get_users_tariffs_info(users):
    basic_users = len([user.id for user in users if user.tariff == 'basic'])
    premium_users = len([user.id for user in users if user.tariff == 'premium'])
    premium_max_users = len([user.id for user in users if user.tariff == 'premium_max'])
    return basic_users, premium_users, premium_max_users


def get_users_online_today(users):
    today = datetime.now().date()
    users = [user.id for user in users if user.last_visit.date() == today]
    return len(users)


def get_users_online_on_this_week(users):
    old_day = datetime.now().date() - timedelta(days=7)
    users = [user.id for user in users if user.last_visit.date() > old_day]
    return len(users)


def get_users_online_on_this_month(users):
    this_year = datetime.now().year
    this_month = datetime.now().month
    users = [user.id for user in users if user.last_visit.year == this_year and user.last_visit.month == this_month]
    return len(users)


def get_users_online_on_this_year(users):
    this_year = datetime.now().year
    users = [user.id for user in users if user.last_visit.year == this_year]
    return len(users)


def get_number_of_active_promo_codes(auto_schools):
    promo_codes = [school.id for school in auto_schools if school.secret_key != school.promo_code]
    return len(promo_codes)


def get_number_of_promo_code_used_users(users):
    promo_code_used_users = [user.id for user in users if user.discount == 1]
    return len(promo_code_used_users)


def get_number_of_pay_orders():
    database_initialization()
    pay_orders = PayOrder.select().count()
    return pay_orders


def get_number_of_payed_users():
    database_initialization()
    payed_users_count = PayOrder.select(PayOrder.telegram_id).distinct().count()
    return payed_users_count


def get_promo_code_conversion(users):
    all_users_len = get_number_of_users()
    promo_code_used_users = get_number_of_promo_code_used_users(users)
    try:
        conversion = round(promo_code_used_users * 100 / all_users_len, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_pay_conversion():
    all_users_len = get_number_of_users()
    payed_users = get_number_of_payed_users()
    try:
        conversion = round(payed_users * 100 / all_users_len, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_ru_language_users_count():
    ru_users = User.select().where(User.language == 'RU').count()
    return ru_users


def get_kz_language_users_count():
    kz_users = User.select().where(User.language == 'KZ').count()
    return kz_users


def get_percent_of_language_choice():
    all_users_len = get_number_of_users()
    ru_users = get_ru_language_users_count()
    kz_users = get_kz_language_users_count()
    result_ru = round(ru_users * 100 / all_users_len, 2)
    result_kz = round(kz_users * 100 / all_users_len, 2)
    return result_ru, result_kz


def get_number_of_users_from_russia():
    ru_users = User.select().where(User.country == 'RU').count()
    return ru_users


def get_number_of_users_from_kazakhstan():
    kz_users = User.select().where(User.country == 'KZ').count()
    return kz_users


def get_percent_of_country_choice():
    all_users_len = get_number_of_users()
    ru_users = get_number_of_users_from_russia()
    kz_users = get_number_of_users_from_kazakhstan()
    result_ru = round(ru_users * 100 / all_users_len, 2)
    result_kz = round(kz_users * 100 / all_users_len, 2)
    return result_ru, result_kz


def get_number_of_auto_schools():
    schools = AutoSchool.select().count()
    return schools


def get_number_of_active_auto_schools(auto_schools):
    auto_schools = get_number_of_active_promo_codes(auto_schools)
    return auto_schools


def get_active_auto_schools_conversion(auto_schools):
    auto_schools_len = get_number_of_auto_schools()
    active_auto_schools = get_number_of_active_auto_schools(auto_schools)
    conversion = round(active_auto_schools * 100 / auto_schools_len, 2)
    return conversion


def get_big_statistics() -> str:
    """
    Получить всю статистику
    :return: Статистику в строков представлении
    """
    users = get_all_users_in_db()
    auto_schools = get_all_auto_schools_on_db()

    users_len = get_number_of_users()
    active_users_len = get_number_of_active_users()
    leavers_len = get_number_of_leavers()
    percentage_active_users, percentage_leavers = get_percentage_between_active_and_liveried_users(users_len,
                                                                                                   active_users_len,
                                                                                                   leavers_len)
    users_today = get_number_of_registrations_today(users)
    users_on_week = get_number_of_registrations_on_week(users)
    users_on_month = get_number_of_registrations_on_month(users)
    users_on_year = get_number_of_registrations_on_year(users)

    users_online_today = get_users_online_today(users)
    users_online_on_this_week = get_users_online_on_this_week(users)
    users_online_on_this_month = get_users_online_on_this_month(users)
    users_online_on_this_year = get_users_online_on_this_year(users)

    basic_users, premium_users, premium_max_users = get_users_tariffs_info(users)

    number_of_pay_orders = get_number_of_pay_orders()
    promo_code_conversion = get_promo_code_conversion(users)

    payed_users = get_number_of_payed_users()
    pay_conversion = get_pay_conversion()
    ru_language_users, kz_language_users = get_percent_of_language_choice()
    users_from_russia, users_from_kazakhstan = get_percent_of_country_choice()

    all_auto_schools = get_number_of_auto_schools()
    active_auto_schools = get_number_of_active_auto_schools(auto_schools)
    active_auto_schools_conversion = get_active_auto_schools_conversion(auto_schools)

    text = [
        f'Пользователей',
        f'Всего: {users_len}',
        f'Активных: {active_users_len} - {percentage_active_users} %',
        f'Ливеров: {leavers_len} - {percentage_leavers} %',
        f'Тариф Базовый: {basic_users}',
        f'Тариф Премиум: {premium_users}',
        f'Тариф Премиум Max: {premium_max_users}',
        '',
        'Регистраций',
        f'Сегодня: {users_today}',
        f'За неделю: {users_on_week}',
        f'За месяц: {users_on_month}',
        f'За год: {users_on_year}',
        ' ',
        f'Онлайн',
        f'Сегодня: {users_online_today}',
        f'За неделю: {users_online_on_this_week}',
        f'За месяц: {users_online_on_this_month}',
        f'За год: {users_online_on_this_year}',
        f' ',
        f'Промо-коды',
        f'Воспользовались {promo_code_conversion} % пользователей',
        f' ',
        f'Автошколы',
        f'Всего: {all_auto_schools}',
        f'Активных: {active_auto_schools}',
        f'Конверсия: {active_auto_schools_conversion} %',
        f' ',
        f'Платежи',
        f'Зарегистрировано: {number_of_pay_orders}',
        f'Оплатили {payed_users} человек',
        f'{pay_conversion} % пользователей',
        f' ',
        f'Из России: {users_from_russia} %',
        f'Из Казахстана: {users_from_kazakhstan} %',
        f' ',
        f'Русскоязычных: {ru_language_users} %',
        f'Казахоязычных: {kz_language_users} %'
    ]

    return '\n'.join(text)


def get_commands_descriptions_and_language_code(command: str) -> dict:
    """
    Получить локализованное описание комманд и код языка
    :param command: комманда
    :return: описание комманд и код языка
    """
    descriptions = ''
    if command == 'set_commands':
        descriptions = COMMANDS_DESCRIPTIONS['ALL']
    elif command == 'set_commands_ru':
        descriptions = COMMANDS_DESCRIPTIONS['RU']
    elif command == 'set_commands_kz':
        descriptions = COMMANDS_DESCRIPTIONS['KZ']
    return descriptions


if __name__ == '__main__':
    # create_database(config.DB_CONFIGS["db_name"])
    # create_new_tables(table_names)
    # set_users_from_backup()
    # set_auto_schools_from_backup()
    write_all_questions_in_db('backup/all_questions_ru.json', 'RU')
    write_all_questions_in_db('backup/all_questions_kz.json', 'KZ')
