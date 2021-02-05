import json
import peewee
import random
from db_models import *
from datetime import datetime, timedelta
import config
import pickle
from google_trans_new import google_translator
from google_trans_new.google_trans_new import google_new_transError

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


# ПЕРЕВОД ------------------------------------------------------------------------------------------------------------


translator = google_translator(timeout=30)


def translate_to_kz(text):
    translated_text = translator.translate(text, lang_src='ru', lang_tgt='kk')
    return translated_text


def translate_list_to_kz(questions_list):
    translated_list = list(map(lambda x: translator.translate(x, lang_src='ru', lang_tgt='kk').strip(), questions_list))
    return translated_list


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
        json.dump(questions_list, json_file, ensure_ascii=False)


def create_null_json_file(json_file_name):
    null_list = []
    with open(json_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(null_list, json_file, ensure_ascii=False)


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


# ТАБЛИЦЫ ------------------------------------------------------------------------------------------------------------


table_names = [Users, QuestionsRU, QuestionsKZ, PromoCodes]


def create_new_tables(db_models):
    try:
        db.connect()
        db.create_tables(db_models)
    except peewee.InternalError as px:
        print(str(px))


# ВОПРОСЫ ------------------------------------------------------------------------------------------------------------


# new_ru_question(question, correct_answer, all_answers, explanation=None, image_code=None)
def new_ru_question(question, correct_answer, all_answers, explanation=None, image_code=None):
    new_question = QuestionsRU(question=question,
                               correct_answer=correct_answer,
                               all_answers=all_answers,
                               explanation=explanation,
                               image_code=image_code
                               )
    new_question.save()


def new_kz_question(question, correct_answer, all_answers, explanation=None, image_code=None):
    new_question = QuestionsKZ(question=question,
                               correct_answer=correct_answer,
                               all_answers=all_answers,
                               explanation=explanation,
                               image_code=image_code
                               )
    new_question.save()


def get_table_length(db_name):
    db_all = db_name.select()
    count = len(db_all)
    return count


def questions_to_db(raw_db, language):
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


def choose_db_by_language(user_language):
    if user_language == 'RU':
        return QuestionsRU
    elif user_language == 'KZ':
        return QuestionsKZ


def get_random_question(user_language):
    db_name = choose_db_by_language(user_language)
    table_length = get_table_length(db_name)
    random_id = random.randrange(1, table_length + 1)
    question_block = db_name.get(db_name.id == random_id)

    question_id = question_block.id
    question = question_block.question
    options = pickle.loads(question_block.all_answers)
    random.shuffle(options)
    correct_option_id = options.index(question_block.correct_answer)
    explanation = question_block.explanation
    image_code = question_block.image_code

    question_dict = {'id': question_id,
                     'question': question,
                     'options': options,
                     'correct_option_id': correct_option_id,
                     'explanation': explanation,
                     'image_code': image_code
                     }
    return question_dict


def get_all_questions_from_db(user_language):
    db_name = choose_db_by_language(user_language)
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


# new_user(778899, 'Bolat')
def new_user(telegram_id, full_name):
    try:
        user = Users(telegram_id=telegram_id, full_name=full_name)
        user.save()
    except peewee.IntegrityError:
        pass


def check_id(telegram_id):
    all_users = all_users_id()
    if telegram_id in all_users:
        return True
    else:
        return False


def all_users_id():
    users_id_list = []
    all_users = Users.select()
    for user in all_users:
        users_id_list.append(user.telegram_id)
    return users_id_list


def get_user_language(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    return user.language


def get_user_country(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    return user.country


# user_language = 'RU' or 'KZ'
def edit_user_language(telegram_id, user_language):
    query = Users.update(language=user_language).where(Users.telegram_id == telegram_id)
    query.execute()


def edit_user_country(telegram_id, user_country):
    query = Users.update(country=user_country).where(Users.telegram_id == telegram_id)
    query.execute()


def get_user_time_limit(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    date_time = user.time_limit
    return date_time


def up_user_time_limit_7days(telegram_id):
    query = Users.update(time_limit=datetime.now() + timedelta(days=7)).where(Users.telegram_id == telegram_id)
    query.execute()


def up_user_time_limit_1years(telegram_id):
    query = Users.update(time_limit=datetime.now() + timedelta(days=365)).where(Users.telegram_id == telegram_id)
    query.execute()


def up_admin_time_limit_3minute():
    query = Users.update(time_limit=datetime.now() + timedelta(minutes=3)).where(Users.telegram_id == config.ADMIN_ID)
    query.execute()


def get_time_visit(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    return user.last_visit


def update_time_visit(telegram_id):
    query = Users.update(last_visit=datetime.now()).where(Users.telegram_id == telegram_id)
    query.execute()


def get_loser_list_14days():
    loser_list = []
    all_users = Users.select()
    for user in all_users:
        telegram_id = user.telegram_id
        time_limit = get_user_time_limit(telegram_id)
        two_week_ago = time_limit + timedelta(days=14)
        if datetime.now() >= two_week_ago:
            loser_list.append(telegram_id)
    return loser_list


def get_loser_list_45days():
    loser_list = []
    all_users = Users.select()
    for user in all_users:
        telegram_id = user.telegram_id
        time_limit = get_user_time_limit(telegram_id)
        two_week_ago = time_limit + timedelta(days=45)
        if datetime.now() >= two_week_ago:
            loser_list.append(telegram_id)
    return loser_list


# ПРОМО КОДЫ ---------------------------------------------------------------------------------------------------------


def all_promo_codes():
    promo_codes_list = []
    promo_codes = PromoCodes.select()
    for promo_code in promo_codes:
        promo_codes_list.append(promo_code.promo_code)
    return promo_codes_list


def check_promo_code(promo_code):
    promo_codes = all_promo_codes()
    if promo_code in promo_codes:
        return True
    else:
        return False


def set_new_promo_code(school_name, secret_key):
    new_promo_code = PromoCodes(school_name=school_name,
                                secret_key=secret_key,
                                promo_code=secret_key
                                )
    new_promo_code.save()


def get_number_of_references(promo_code):
    promo_code = PromoCodes.get(PromoCodes.promo_code == promo_code)
    number_of_references = promo_code.number_of_references
    return number_of_references


def up_number_of_references(promo_code):
    query = PromoCodes.update(number_of_references=PromoCodes.number_of_references + 1).where(
        PromoCodes.promo_code == promo_code)
    query.execute()


def filter_by(text):
    text = text.upper()
    text = [c for c in text if c in 'QWERTYUIOPASDFGHJKLZXCVBNM.-_, 1234567890+#№$!%&?*']
    return ''.join(text)


def uppercase_check(text):
    upper_text = filter_by(text)
    if text == upper_text:
        return True
    else:
        return False


# СТАТИСТИКА ---------------------------------------------------------------------------------------------------------


def get_number_of_users():
    all_users = Users.select()
    number_of_users = len(all_users)
    return number_of_users


def get_number_of_users_on_day():
    today = datetime.now().date()
    all_users = Users.select().where(Users.registration_date == today)
    number_of_users = len(all_users)
    return number_of_users


def get_number_of_users_on_week():
    old_day = datetime.now().date() - timedelta(days=7)
    all_users = Users.select().where(Users.registration_date > old_day)
    number_of_users = len(all_users)
    return number_of_users


def get_number_of_users_on_month():
    this_month = datetime.now().month
    this_year = datetime.now().year
    users_count = 0
    all_users = Users.select()
    for user in all_users:
        if user.registration_date.year == this_year and user.registration_date.month == this_month:
            users_count += 1
    return users_count


def get_number_of_users_on_year():
    this_year = datetime.now().year
    users_count = 0
    all_users = Users.select()
    for user in all_users:
        if user.registration_date.year == this_year:
            users_count += 1
    return users_count


def get_users_online_now():
    today = datetime.now()
    users_online = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month and user.last_visit.hour == today.hour:
            users_online += 1
    return users_online


def get_users_online_today():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month and user.last_visit.day == today.day:
            count += 1
    return count


def get_users_online_on_this_week():
    old_day = datetime.now() - timedelta(days=7)
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.date() > old_day.date():
            count += 1
    return count


def get_users_online_on_this_month():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month:
            count += 1
    return count


def get_users_online_on_this_year():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year:
            count += 1
    return count


def get_all_users_list():
    result = []
    all_users = Users.select()
    result.append('id -> имя')
    for user in all_users:
        result.append(f"{user.telegram_id} -> {user.full_name}")
    return '\n'.join(result)


def get_number_of_promo_codes():
    promo_codes = PromoCodes.select()
    number_of_promo_codes = len(promo_codes)
    return number_of_promo_codes


def get_number_of_promo_codes_on_day():
    today = datetime.now().date()
    promo_codes = PromoCodes.select().where(PromoCodes.registration_date == today)
    number_of_promo_codes = len(promo_codes)
    return number_of_promo_codes


def get_number_of_promo_codes_on_week():
    old_day = datetime.now().date() - timedelta(days=7)
    promo_codes = PromoCodes.select().where(PromoCodes.registration_date > old_day)
    number_of_promo_codes = len(promo_codes)
    return number_of_promo_codes


def get_number_of_promo_codes_on_month():
    this_month = datetime.now().month
    this_year = datetime.now().year
    promo_codes_count = 0
    promo_codes = PromoCodes.select()
    for promo_code in promo_codes:
        if promo_code.registration_date.year == this_year and promo_code.registration_date.month == this_month:
            promo_codes_count += 1
    return promo_codes_count


def get_number_of_promo_codes_on_year():
    this_year = datetime.now().year
    promo_codes_count = 0
    promo_codes = PromoCodes.select()
    for promo_code in promo_codes:
        if promo_code.registration_date.year == this_year:
            promo_codes_count += 1
    return promo_codes_count


def get_all_promo_code_list():
    result = []
    promo_codes = PromoCodes.select().order_by(PromoCodes.number_of_references.desc())
    result.append('школа > промо-код > упоминаний')
    for promo_code in promo_codes:
        result.append(f"{promo_code.school_name} {promo_code.promo_code} {promo_code.number_of_references}")
    return '\n'.join(result)


def get_number_of_promo_code_used_users():
    promo_code_used_users = Users.select().where(Users.promo_code_used is True)
    promo_code_used = len(promo_code_used_users)
    return promo_code_used


def get_number_of_payed_users():
    payed_users = Users.select().where(Users.made_payment is True)
    payed_users_count = len(payed_users)
    return payed_users_count


def get_promo_code_conversion():
    users = get_number_of_users()
    promo_code_used_users = get_number_of_promo_code_used_users()
    try:
        conversion = round(promo_code_used_users * 100 / users, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_pay_conversion():
    users = get_number_of_users()
    payed_users = get_number_of_payed_users()
    try:
        conversion = round(payed_users * 100 / users, 2)
    except ZeroDivisionError:
        conversion = 0
    return conversion


def get_ru_language_users_count():
    ru_users = Users.select().where(Users.language == 'RU')
    ru_users_count = len(ru_users)
    return ru_users_count


def get_kz_language_users_count():
    kz_users = Users.select().where(Users.language == 'KZ')
    kz_users_count = len(kz_users)
    return kz_users_count


def get_percent_of_language_choice():
    users = get_number_of_users()
    ru_users = get_ru_language_users_count()
    kz_users = get_kz_language_users_count()
    result_ru = round(ru_users * 100 / users, 2)
    result_kz = round(kz_users * 100 / users, 2)
    return result_ru, result_kz


def get_russian_users_count():
    ru_users = Users.select().where(Users.country == 'RU')
    ru_users_count = len(ru_users)
    return ru_users_count


def get_kazakhstan_users_count():
    kz_users = Users.select().where(Users.country == 'KZ')
    kz_users_count = len(kz_users)
    return kz_users_count


def get_percent_of_country_choice():
    users = get_number_of_users()
    ru_users = get_russian_users_count()
    kz_users = get_kazakhstan_users_count()
    result_ru = round(ru_users * 100 / users, 2)
    result_kz = round(kz_users * 100 / users, 2)
    return result_ru, result_kz


def get_big_statistics():
    users = get_number_of_users()
    users_today = get_number_of_users_on_day()
    users_on_week = get_number_of_users_on_week()
    users_on_month = get_number_of_users_on_month()
    users_on_year = get_number_of_users_on_year()

    users_online = get_users_online_now()
    users_online_today = get_users_online_today()
    users_online_on_this_week = get_users_online_on_this_week()
    users_online_on_this_month = get_users_online_on_this_month()
    users_online_on_this_year = get_users_online_on_this_year()

    promo_codes = get_number_of_promo_codes()
    promo_codes_today = get_number_of_promo_codes_on_day()
    promo_codes_on_week = get_number_of_promo_codes_on_week()
    promo_codes_on_month = get_number_of_promo_codes_on_month()
    promo_codes_on_year = get_number_of_promo_codes_on_year()

    promo_code_conversion = get_promo_code_conversion()
    pay_conversion = get_pay_conversion()
    ru_language_users, kz_language_users = get_percent_of_language_choice()
    users_from_russia, users_from_kazakhstan = get_percent_of_country_choice()

    text = [
        f'Зарегистрированных пользователей: {users}',
        f'Зарегистрировались сегодня: {users_today}',
        f'Зарегистрировались на этой неделе: {users_on_week}',
        f'Зарегистрировались в этом месяце: {users_on_month}',
        f'Зарегистрировались за год: {users_on_year}',
        '\n',
        f'Cейчас онлайн: {users_online}',
        f'Сегодня были в онлайн: {users_online_today}',
        f'Онлайн за неделю: {users_online_on_this_week}',
        f'Онлайн за месяц: {users_online_on_this_month}',
        f'Онлайн за год: {users_online_on_this_year}',
        '\n'
        f'Зарегистрировано промо-кодов: {promo_codes}',
        f'Зарегистрировано промо-кодов сегодня: {promo_codes_today}',
        f'Зарегистрировано промо-кодов на этой неделе: {promo_codes_on_week}',
        f'Зарегистрировано промо-кодов в этом месяце: {promo_codes_on_month}',
        f'Зарегистрировано промо-кодов за год: {promo_codes_on_year}',
        f'Воспользовались промо-кодами: {promo_code_conversion}% пользователей',
        f'\n',
        f'Оплатили сервис: {pay_conversion}% пользователей',
        f'\n',
        f'Пользователей в России: {users_from_russia}%',
        f'Пользователей в Казахстане: {users_from_kazakhstan}%',
        f'Из них:',
        f'Русскоязычных пользователей: {ru_language_users}%',
        f'Казахоязычных пользователей: {kz_language_users}%'
    ]

    return '\n'.join(text)


if __name__ == '__main__':
    create_new_tables(table_names)
    # write_all_questions_in_db('all_questions_ru.json', 'RU')
    # write_all_questions_in_db('all_questions_kz.json', 'KZ')
