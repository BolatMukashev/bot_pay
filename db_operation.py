import os
import json
import peewee
import random
import string
from db_models import *
from datetime import datetime, timedelta
import config
import pickle
from google_trans_new import google_translator
from google_trans_new.google_trans_new import google_new_transError
from messages import MESSAGE

# ТАБЛИЦЫ ------------------------------------------------------------------------------------------------------------


table_names = [Users, QuestionsRU, QuestionsKZ, AutoSchools]


def create_new_tables(db_models):
    try:
        db.connect()
        db.create_tables(db_models)
        print('Таблицы созданы...')
    except peewee.InternalError as err:
        print(str(err))


def create_database(db_name):
    try:
        conn.cursor().execute(f'create database {db_name}')
        print('База данных успешно создана...')
    except pymysql.err.ProgrammingError:
        print('База данных уже была создана ранее...')


def database_initialization():
    if not db.is_closed():
        db.close()


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
    QuestionsRU.update(image_code=new_code).where(QuestionsRU.image_code == old_code).execute()
    QuestionsKZ.update(image_code=new_code).where(QuestionsKZ.image_code == old_code).execute()


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
    new_question = QuestionsRU(question=question,
                               correct_answer=correct_answer,
                               all_answers=all_answers,
                               explanation=explanation,
                               image_code=image_code
                               )
    new_question.save()


def new_kz_question(question, correct_answer, all_answers, explanation=None, image_code=None):
    database_initialization()
    new_question = QuestionsKZ(question=question,
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
    print(f'Вопросы добавлены в таблицу {language}...\nНе забудь закомментировать эту строку кода!')


def choose_db_by_language(user_language):
    if user_language == 'RU':
        return QuestionsRU
    elif user_language == 'KZ':
        return QuestionsKZ


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


def new_user(telegram_id: int, full_name: str) -> None:
    """Добавить нового пользователя в базу"""
    database_initialization()
    try:
        user = Users(telegram_id=telegram_id, full_name=full_name, price_in_rubles=config.BASE_PRICE)
        user.save()
    except peewee.IntegrityError:
        pass


def set_user_on_db(telegram_id, full_name, country, language, registration_date, registration_is_over, time_limit,
                   last_visit, promo_code_used, price_in_rubles, made_payment, second_week_promotional_offer,
                   sixth_week_promotional_offer):
    """Это когда добавляешь пользователя из JSON файла в базу (гавнокод), нужно будет переписать.
    Спарсить всех пользователей из JSON файла модулем Pydantic и передавать сюда 1 параметр типа object"""
    registration_date = convert_str_to_datetime(registration_date)
    time_limit = convert_str_to_datetime(time_limit)
    last_visit = convert_str_to_datetime(last_visit)
    try:
        database_initialization()
        user = Users(telegram_id=telegram_id,
                     full_name=full_name,
                     country=country,
                     language=language,
                     registration_date=registration_date,
                     registration_is_over=registration_is_over,
                     time_limit=time_limit,
                     last_visit=last_visit,
                     promo_code_used=promo_code_used,
                     price_in_rubles=price_in_rubles,
                     made_payment=made_payment,
                     second_week_promotional_offer=second_week_promotional_offer,
                     sixth_week_promotional_offer=sixth_week_promotional_offer)
        user.save()
    except peewee.IntegrityError:
        pass


def check_id(telegram_id):
    all_users = get_all_users_telegram_id()
    if telegram_id in all_users:
        return True
    else:
        return False


def valid_id(telegram_id):
    if str(telegram_id).isdigit():
        return True


def get_user_by(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user


def get_all_users_in_db() -> object:
    """
    Получить всех пользователей из базы данных (для статистики)
    :return: Данные о всех пользователях из базы
    """
    database_initialization()
    users = Users.select()
    return users


def get_user_name_by(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.full_name


def get_user_language(telegram_id):
    """Получить язык пользователя из кэша/базы"""
    user_language = config.users_data_cache.get(telegram_id)
    if user_language:
        return user_language
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    config.users_data_cache[telegram_id] = user.language
    return user.language


# database_initialization - надо бы в декоратор завернуть
def edit_user_language(telegram_id: int, new_user_language) -> None:
    """
    :param telegram_id: telegram_id
    :param new_user_language: 'RU' or 'KZ'
    """
    database_initialization()
    query = Users.update(language=new_user_language).where(Users.telegram_id == telegram_id)
    query.execute()
    config.users_data_cache[telegram_id] = new_user_language


def get_user_country(telegram_id: int) -> str:
    """Получить страну пользователя из базы"""
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.country


def edit_user_country(telegram_id, user_country):
    database_initialization()
    query = Users.update(country=user_country).where(Users.telegram_id == telegram_id)
    query.execute()


def get_monetary_unit_by_user_country(telegram_id):
    database_initialization()
    user = get_user_by(telegram_id)
    user_country = user.country
    user_language = user.language
    if user_country == 'KZ':
        return 'тенге'
    elif user_country == 'RU' and user_language == 'RU':
        return 'рублей'
    elif user_country == 'RU' and user_language == 'KZ':
        return 'рубль'
    else:
        return 'рублей'


# для платежки kassa24
def get_monetary_unit(user_country, user_language):
    if user_country == 'KZ':
        return 'тенге'
    elif user_country == 'RU' and user_language == 'RU':
        return 'рублей'
    elif user_country == 'RU' and user_language == 'KZ':
        return 'рубль'
    else:
        return 'рублей'


class PayOrder:
    def __init__(self, user_country: str, user_language: str, price_in_rubles: int):
        """
        Прием оплаты в рублях не работает (платежная система IOKA)
        (398 - код тенге, 643 - код рубля)
        :param user_country: Страна пользователя
        :param user_language: Язык пользователя
        """
        self.user_country = user_country
        self.user_language = user_language
        self.price_ruble = price_in_rubles
        self.price_tenge = int(self.price_ruble * config.RUBLES_EXCHANGE_RATE)
        self.code = 398

        if self.user_country == 'KZ':
            self.message_text = MESSAGE[f'pay_message_{self.user_language}'] + f' {self.price_tenge} тенге!'

        elif self.user_country == 'RU' and self.user_language == 'RU':
            self.message_text = MESSAGE[f'pay_message_{self.user_language}'] + f' {self.price_ruble} рублей!' \
                                                                               f' ({self.price_tenge} тенге)'

        elif self.user_country == 'RU' and self.user_language == 'KZ':
            self.message_text = MESSAGE[f'pay_message_{self.user_language}'] + f' {self.price_ruble} рубль!' \
                                                                               f' ({self.price_tenge} тенге)'


def get_user_time_limit(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
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


def up_user_time_limit_days(telegram_id, days: int) -> None:
    """Продлить доступ к боту на n дней"""
    time_limit_is_over = user_time_limit_is_over(telegram_id)
    if time_limit_is_over:
        query = Users.update(time_limit=datetime.now() + timedelta(days=days)).where(Users.telegram_id == telegram_id)
    else:
        time_limit_date = get_user_time_limit(telegram_id)
        query = Users.update(time_limit=time_limit_date + timedelta(days=days)).where(Users.telegram_id == telegram_id)
    query.execute()


def up_admin_time_limit_3minute():
    database_initialization()
    query = Users.update(time_limit=datetime.now() + timedelta(minutes=3)).where(Users.telegram_id == config.ADMIN_ID)
    query.execute()


def get_time_visit(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.last_visit


def get_price_in_rubles_on_user(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.price_ruble


def get_finally_price(telegram_id):
    database_initialization()
    user = get_user_by(telegram_id)
    price_in_rubles = user.price_ruble
    user_country = user.country
    if user_country == 'KZ':
        return round(price_in_rubles * 5)
    else:
        return price_in_rubles


def get_finally_price_by(price_in_rubles: int, user_country: str) -> int:
    """
    Преобразует цену в рублях в цену в тенге, если пользователь из Казахстана
    :param price_in_rubles: Цена из базы, у пользователя, в рублях
    :param user_country: Страна проживания пользователя
    :return:
    """
    if user_country == 'KZ':
        return int(price_in_rubles * config.RUBLES_EXCHANGE_RATE)
    else:
        return price_in_rubles


def change_price_in_rubles_on_user(telegram_id, new_price):
    database_initialization()
    query = Users.update(price_in_rubles=new_price).where(Users.telegram_id == telegram_id)
    query.execute()


def get_user_registration_status(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.registration_is_over


def update_registration_status(telegram_id):
    database_initialization()
    query = Users.update(registration_is_over=True).where(Users.telegram_id == telegram_id)
    query.execute()


def update_second_week_promotional_offer_status(telegram_id):
    database_initialization()
    query = Users.update(second_week_promotional_offer=True).where(Users.telegram_id == telegram_id)
    query.execute()


def update_sixth_week_promotional_offer_status(telegram_id):
    database_initialization()
    query = Users.update(sixth_week_promotional_offer=True).where(Users.telegram_id == telegram_id)
    query.execute()


def get_user_promo_code_used_status(telegram_id):
    database_initialization()
    user = Users.get(Users.telegram_id == telegram_id)
    return user.promo_code_used


def update_user_promo_code_used_status(telegram_id):
    database_initialization()
    query = Users.update(promo_code_used=True).where(Users.telegram_id == telegram_id)
    query.execute()


def update_user_made_payment_status(telegram_id):
    database_initialization()
    query = Users.update(made_payment=True).where(Users.telegram_id == telegram_id)
    query.execute()


def update_time_visit(telegram_id):
    database_initialization()
    query = Users.update(last_visit=datetime.now()).where(Users.telegram_id == telegram_id)
    query.execute()


def get_all_users_telegram_id(language: str = '', country: str = '') -> list:
    """
    Получить telegram_id пользователей (фильтр по языку)
    :param language: Язык пользователей
    :param country: Страна пользователей
    :return: список id пользователей
    """
    database_initialization()
    if language:
        users = Users.select(Users.telegram_id).where(Users.language == language)
    elif country:
        users = Users.select(Users.telegram_id).where(Users.country == country)
    else:
        users = Users.select(Users.telegram_id)
    telegram_ids = [user.telegram_id for user in users]
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


def get_loser_list_14days():
    loser_list = []
    database_initialization()
    all_users = Users.select().where(Users.second_week_promotional_offer == 0)
    for user in all_users:
        telegram_id = user.telegram_id
        time_limit = get_user_time_limit(telegram_id)
        two_week_ago = time_limit + timedelta(days=14)
        if datetime.now() > two_week_ago:
            loser_list.append(telegram_id)
    return loser_list


def get_loser_list_45days():
    loser_list = []
    database_initialization()
    all_users = Users.select().where(Users.sixth_week_promotional_offer == 0)
    for user in all_users:
        telegram_id = user.telegram_id
        time_limit = get_user_time_limit(telegram_id)
        two_week_ago = time_limit + timedelta(days=45)
        if datetime.now() > two_week_ago:
            loser_list.append(telegram_id)
    return loser_list


def get_all_users_on_dict_format():
    all_users_list = []
    database_initialization()
    all_users = Users.select()
    for user in all_users:
        simple_user = {'id': user.id,
                       'telegram_id': user.telegram_id,
                       'full_name': user.full_name,
                       'country': user.country,
                       'language': user.language,
                       'registration_date': user.registration_date,
                       'registration_is_over': user.registration_is_over,
                       'time_limit': user.time_limit,
                       'last_visit': user.last_visit,
                       'promo_code_used': user.promo_code_used,
                       'price_in_rubles': user.price_ruble,
                       'made_payment': user.made_payment,
                       'second_week_promotional_offer': user.second_week_promotional_offer,
                       'sixth_week_promotional_offer': user.sixth_week_promotional_offer}
        all_users_list.append(simple_user)
    return all_users_list


# ПРОМО КОДЫ ---------------------------------------------------------------------------------------------------------


def all_promo_codes():
    promo_codes_list = []
    database_initialization()
    promo_codes = AutoSchools.select()
    for promo_code in promo_codes:
        promo_codes_list.append(promo_code.promo_code)
    return promo_codes_list


def check_promo_code(promo_code):
    promo_codes = all_promo_codes()
    if promo_code in promo_codes:
        return True
    else:
        return False


def edit_promo_code(secret_key, new_promo_code):
    database_initialization()
    query = AutoSchools.update(promo_code=new_promo_code).where(AutoSchools.secret_key == secret_key)
    query.execute()


# промокод меняет владелец автошколы, доступ к промкоду по secret_key
def set_auto_schools_in_db(auto_schools):
    for auto_school in auto_schools:
        school_name = auto_school['school_name']
        country = auto_school['country']
        city = auto_school['city']
        phones = pickle.dumps(auto_school['phones'], pickle.HIGHEST_PROTOCOL)
        emails = pickle.dumps(auto_school['emails'], pickle.HIGHEST_PROTOCOL)
        secret_key = get_unique_secret_key()
        promo_code = secret_key
        add_new_auto_school(school_name, country, city, phones, emails, secret_key, promo_code)


def add_new_auto_school(school_name, country, city, phones, emails, secret_key, promo_code):
    database_initialization()
    new_auto_school = AutoSchools(school_name=school_name,
                                  country=country,
                                  city=city,
                                  phones=phones,
                                  emails=emails,
                                  secret_key=secret_key,
                                  promo_code=promo_code
                                  )
    new_auto_school.save()


def add_auto_school_on_db(school_name, country, city, phones, emails, registration_date, secret_key, promo_code,
                          number_of_references, notified):
    database_initialization()
    auto_school = AutoSchools(school_name=school_name,
                              country=country,
                              city=city,
                              phones=pickle.dumps(phones, pickle.HIGHEST_PROTOCOL),
                              emails=pickle.dumps(emails, pickle.HIGHEST_PROTOCOL),
                              registration_date=convert_str_to_date(registration_date),
                              secret_key=secret_key,
                              promo_code=promo_code,
                              number_of_references=number_of_references,
                              notified=notified
                              )
    try:
        auto_school.save()
    except peewee.IntegrityError:
        pass


def get_all_auto_schools_on_db():
    database_initialization()
    all_auto_schools = AutoSchools.select()
    return all_auto_schools


def get_auto_school_by(secret_key):
    database_initialization()
    school = AutoSchools.get(AutoSchools.secret_key == secret_key)
    return school


def get_auto_school_emails_by(secret_key):
    database_initialization()
    school = AutoSchools.get(AutoSchools.secret_key == secret_key)
    emails = pickle.loads(school.emails)
    return emails


def get_all_auto_schools_emails():
    emails = []
    database_initialization()
    schools = AutoSchools.select()
    for school in schools:
        email = pickle.loads(school.emails)
        emails.extend(email)
    return emails


def delete_auto_schools_by(secret_key):
    database_initialization()
    query = AutoSchools.delete().where(AutoSchools.secret_key == secret_key)
    query.execute()


def get_not_notified_auto_schools():
    database_initialization()
    auto_schools = AutoSchools.select().where(AutoSchools.notified == 0)
    return auto_schools


def get_all_auto_schools_on_dict_format(auto_schools_in_db):
    all_schools = []
    for school in auto_schools_in_db:
        data = {'id': school.id,
                'school_name': school.school_name,
                'country': school.country,
                'city': school.city,
                'phones': pickle.loads(school.phones),
                'emails': pickle.loads(school.emails),
                'registration_date': school.registration_date,
                'secret_key': school.secret_key,
                'promo_code': school.promo_code,
                'number_of_references': school.number_of_references,
                'notified': school.notified}
        all_schools.append(data)
    return all_schools


def get_not_notified_auto_schools_emails():
    all_emails = []
    database_initialization()
    auto_schools = get_not_notified_auto_schools()
    schools = get_all_auto_schools_on_dict_format(auto_schools)
    for school in schools:
        for email in school['emails']:
            all_emails.append(email)
    return all_emails


def edit_notified_status(school_id):
    database_initialization()
    query = AutoSchools.update(notified=1).where(AutoSchools.id == school_id)
    query.execute()


def all_secret_keys():
    secret_keys_list = []
    database_initialization()
    promo_codes = AutoSchools.select()
    for promo_code in promo_codes:
        secret_keys_list.append(promo_code.secret_key)
    return secret_keys_list


def check_secret_key(secret_key):
    secret_keys = all_secret_keys()
    if secret_key in secret_keys:
        return True
    else:
        return False


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
    promo_code = AutoSchools.get(AutoSchools.promo_code == promo_code)
    number_of_references = promo_code.number_of_references
    return number_of_references


def up_number_of_references(promo_code):
    database_initialization()
    query = AutoSchools.update(number_of_references=AutoSchools.number_of_references + 1).where(
        AutoSchools.promo_code == promo_code)
    query.execute()


def correct_letters_filter(promo_code):
    promo_code = promo_code.upper()
    correct_promo_code = [c for c in promo_code if c in string.ascii_uppercase + string.digits + '.-_, +#№$!%&?*']
    return ''.join(correct_promo_code)


def promo_code_check_to_correct(promo_code):
    correct_promo_code = correct_letters_filter(promo_code)
    if promo_code == correct_promo_code:
        return True
    else:
        return False


# БЭКАП ДАННЫХ -------------------------------------------------------------------------------------------------------


def path_to_users_backup():
    file_name = 'users.json'
    this_path = os.getcwd()
    path = os.path.join(this_path, 'backup', file_name)
    return path


def path_to_auto_schools_backup():
    file_name = 'auto_schools.json'
    this_path = os.getcwd()
    path = os.path.join(this_path, 'backup', file_name)
    return path


def backup_users():
    all_users = get_all_users_on_dict_format()
    path = path_to_users_backup()
    create_new_json_file(path, all_users)


def backup_auto_schools():
    auto_schools = get_all_auto_schools_on_db()
    all_auto_schools = get_all_auto_schools_on_dict_format(auto_schools)
    path = path_to_auto_schools_backup()
    create_new_json_file(path, all_auto_schools)


def convert_str_to_datetime(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_obj


def convert_str_to_date(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_obj.date()


def set_users_from_backup():
    path = path_to_users_backup()
    users = get_data_from_json_file(path)
    for user in users:
        set_user_on_db(user['telegram_id'], user['full_name'], user['country'], user['language'],
                       user['registration_date'], user['registration_is_over'], user['time_limit'],
                       user['last_visit'], user['promo_code_used'], user['price_in_rubles'], user['made_payment'],
                       user['second_week_promotional_offer'], user['sixth_week_promotional_offer'])


def set_auto_schools_from_backup():
    path = path_to_auto_schools_backup()
    auto_schools = get_data_from_json_file(path)
    for auto_school in auto_schools:
        add_auto_school_on_db(auto_school['school_name'], auto_school['country'], auto_school['city'],
                              auto_school['phones'], auto_school['emails'], auto_school['registration_date'],
                              auto_school['secret_key'], auto_school['promo_code'], auto_school['number_of_references'],
                              auto_school['notified'])


# СТАТИСТИКА ---------------------------------------------------------------------------------------------------------


def get_number_of_users(users) -> int:
    users = [user.id for user in users]
    return len(users)


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


def get_number_of_promo_codes(auto_schools):
    promo_codes = [auto_school.id for auto_school in auto_schools]
    return len(promo_codes)


def get_number_of_activated_promo_codes(auto_schools):
    promo_codes = [auto_school.id for auto_school in auto_schools if auto_school.secret_key != auto_school.promo_code]
    return len(promo_codes)


def get_number_of_promo_codes_registrations_today(auto_schools):
    today = datetime.now().date()
    promo_codes = [auto_school.id for auto_school in auto_schools if auto_school.registration_date.date() == today]
    return len(promo_codes)


def get_number_of_promo_codes_registrations_on_week(auto_schools):
    seven_day_ago = datetime.now().date() - timedelta(days=7)
    promo_codes = [auto_school.id for auto_school in auto_schools if
                   auto_school.registration_date.date() > seven_day_ago]
    return len(promo_codes)


def get_number_of_promo_codes_registrations_on_month(auto_schools):
    this_year = datetime.now().year
    this_month = datetime.now().month
    promo_codes = [auto_school.id for auto_school in auto_schools if
                   auto_school.registration_date.year == this_year and
                   auto_school.registration_date.month == this_month]
    return len(promo_codes)


def get_number_of_promo_codes_registrations_on_year(auto_schools):
    this_year = datetime.now().year
    promo_codes = [auto_school.id for auto_school in auto_schools if auto_school.registration_date.year == this_year]
    return len(promo_codes)


def get_number_of_promo_code_used_users(users):
    promo_code_used_users = [user.id for user in users if user.promo_code_used == 1]
    return len(promo_code_used_users)


def get_number_of_payed_users(users):
    payed_users = [user for user in users if user.made_payment == 1]
    return len(payed_users)


def get_promo_code_conversion(users):
    all_users_len = get_number_of_users(users)
    promo_code_used_users = get_number_of_promo_code_used_users(users)
    try:
        conversion = round(promo_code_used_users * 100 / all_users_len, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_pay_conversion(users):
    all_users_len = get_number_of_users(users)
    payed_users = get_number_of_payed_users(users)
    try:
        conversion = round(payed_users * 100 / all_users_len, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_ru_language_users_count(users):
    ru_users = [user.id for user in users if user.language == 'RU']
    return len(ru_users)


def get_kz_language_users_count(users):
    kz_users = [user.id for user in users if user.language == 'KZ']
    return len(kz_users)


def get_percent_of_language_choice(users):
    all_users_len = get_number_of_users(users)
    ru_users = get_ru_language_users_count(users)
    kz_users = get_kz_language_users_count(users)
    result_ru = round(ru_users * 100 / all_users_len, 2)
    result_kz = round(kz_users * 100 / all_users_len, 2)
    return result_ru, result_kz


def get_number_of_users_from_russia(users):
    ru_users = [user.id for user in users if user.country == 'RU']
    return len(ru_users)


def get_number_of_users_from_kazakhstan(users):
    kz_users = [user.id for user in users if user.country == 'KZ']
    return len(kz_users)


def get_percent_of_country_choice(users):
    all_users_len = get_number_of_users(users)
    ru_users = get_number_of_users_from_russia(users)
    kz_users = get_number_of_users_from_kazakhstan(users)
    result_ru = round(ru_users * 100 / all_users_len, 2)
    result_kz = round(kz_users * 100 / all_users_len, 2)
    return result_ru, result_kz


def get_number_of_auto_schools(auto_schools):
    auto_schools = get_number_of_promo_codes(auto_schools)
    return auto_schools


def get_number_of_active_auto_schools(auto_schools):
    auto_schools = get_number_of_activated_promo_codes(auto_schools)
    return auto_schools


def get_active_auto_schools_conversion(auto_schools):
    auto_schools_len = get_number_of_auto_schools(auto_schools)
    active_auto_schools = get_number_of_active_auto_schools(auto_schools)
    conversion = round(active_auto_schools * 100 / auto_schools_len, 2)
    return conversion


def get_big_statistics():
    users = get_all_users_in_db()
    auto_schools = get_all_auto_schools_on_db()
    users_len = get_number_of_users(users)
    users_today = get_number_of_registrations_today(users)
    users_on_week = get_number_of_registrations_on_week(users)
    users_on_month = get_number_of_registrations_on_month(users)
    users_on_year = get_number_of_registrations_on_year(users)

    users_online_today = get_users_online_today(users)
    users_online_on_this_week = get_users_online_on_this_week(users)
    users_online_on_this_month = get_users_online_on_this_month(users)
    users_online_on_this_year = get_users_online_on_this_year(users)

    promo_codes = get_number_of_promo_codes(auto_schools)
    promo_codes_today = get_number_of_promo_codes_registrations_today(auto_schools)
    promo_codes_on_week = get_number_of_promo_codes_registrations_on_week(auto_schools)
    promo_codes_on_month = get_number_of_promo_codes_registrations_on_month(auto_schools)
    promo_codes_on_year = get_number_of_promo_codes_registrations_on_year(auto_schools)
    promo_code_conversion = get_promo_code_conversion(users)

    payed_users = get_number_of_payed_users(users)
    pay_conversion = get_pay_conversion(users)
    ru_language_users, kz_language_users = get_percent_of_language_choice(users)
    users_from_russia, users_from_kazakhstan = get_percent_of_country_choice(users)

    all_auto_schools = get_number_of_auto_schools(auto_schools)
    active_auto_schools = get_number_of_active_auto_schools(auto_schools)
    active_auto_schools_conversion = get_active_auto_schools_conversion(auto_schools)

    text = [
        f'Зарегистрированных пользователей',
        f'Всего: {users_len}',
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
        f'Зарегистрировано промо-кодов',
        f'Всего: {promo_codes}',
        f'Сегодня: {promo_codes_today}',
        f'За неделю: {promo_codes_on_week}',
        f'За месяц: {promo_codes_on_month}',
        f'За год: {promo_codes_on_year}',
        f'Воспользовались {promo_code_conversion} % пользователей',
        f' ',
        f'Зарегистрировано автошкол',
        f'Всего: {all_auto_schools}',
        f'Активных: {active_auto_schools}',
        f'Конверсия: {active_auto_schools_conversion} %',
        f' ',
        f'Оплатили сервис',
        f'{payed_users} человек',
        f'{pay_conversion} % пользователей',
        f' ',
        f'Из России: {users_from_russia} %',
        f'Из Казахстана: {users_from_kazakhstan} %',
        f' ',
        f'Русскоязычных: {ru_language_users} %',
        f'Казахоязычных: {kz_language_users} %'
    ]

    return '\n'.join(text)


if __name__ == '__main__':
    create_database(config.DB_CONFIGS["db_name"])
    create_new_tables(table_names)
    set_users_from_backup()
    set_auto_schools_from_backup()
    write_all_questions_in_db('backup/all_questions_ru.json', 'RU')
    write_all_questions_in_db('backup/all_questions_kz.json', 'KZ')
