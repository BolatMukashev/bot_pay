import peewee
from db_models import *
import random
from datetime import datetime, timedelta
from config import QUESTION_AVAILABLE, ADMIN_ID
from questions_ru1 import bad_db
import pickle
from google_trans_new import google_translator

# ПЕРЕВОД ------------------------------------------------------------------------------------------------------------

translator = google_translator()


def translate_to_kz(text):
    translated_text = translator.translate(text, lang_src='ru', lang_tgt='kk')
    return translated_text


def translate_list_to_kz(questions_list):
    translated_list = list(map(lambda x: translator.translate(x, lang_src='ru', lang_tgt='kk'), questions_list))
    return translated_list


# ТАБЛИЦЫ ------------------------------------------------------------------------------------------------------------


table_names = [Users, QuestionsRU, QuestionsKZ, PromoCodes, SuperPromoCode]


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


def get_table_lenght(db_name):
    db_all = db_name.select()
    count = len(db_all)
    return count


def questions_to_ru_db(raw_db):
    for el in raw_db:
        question = el['question']
        correct_answer = el['correct_answer']
        all_answers = pickle.dumps(el['all_answers'], pickle.HIGHEST_PROTOCOL)
        explanation = el['explanation']
        image_code = el['img']
        new_ru_question(question, correct_answer, all_answers, explanation, image_code)


def questions_to_kz_db(raw_db):
    for el in raw_db:
        question = translate_to_kz(el['question'])
        correct_answer = translate_to_kz(el['correct_answer'])
        all_answers = pickle.dumps(translate_list_to_kz(el['all_answers']), pickle.HIGHEST_PROTOCOL)
        explanation = 'Дұрыс емес'
        image_code = el['img']
        new_kz_question(question, correct_answer, all_answers, explanation, image_code)


def get_random_question(user_language):
    if user_language == 'RU':
        db_name = QuestionsRU
    elif user_language == 'KZ':
        db_name = QuestionsKZ

    table_lenght = get_table_lenght(db_name)
    random_id = random.randrange(1, table_lenght + 1)
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


def get_all_ru_questions():
    questions = QuestionsRU.select()
    questions_list = []
    for el in questions:
        id = el.id
        question = el.question
        correct_answer = el.correct_answer
        all_answers = pickle.loads(el.all_answers)
        explanation = el.explanation
        image_code = el.image_code
        question_dict = {'id': id, 'question': question, 'correct_answer': correct_answer, 'all_answers': all_answers,
                         'explanation': explanation, 'image_code': image_code}
        questions_list.append(question_dict)
    return questions_list


def get_all_kz_questions():
    questions = QuestionsKZ.select()
    questions_list = []
    for el in questions:
        id = el.id
        question = el.question
        correct_answer = el.correct_answer
        all_answers = pickle.loads(el.all_answers)
        explanation = el.explanation
        image_code = el.image_code
        question_dict = {'id': id, 'question': question, 'correct_answer': correct_answer, 'all_answers': all_answers,
                         'explanation': explanation, 'image_code': image_code}
        questions_list.append(question_dict)
    return questions_list


# ПОЛЬЗОВАТЕЛЬ -------------------------------------------------------------------------------------------------------


# new_user(778899, 'Bolat')
def new_user(telegram_id, user_name):
    try:
        user = Users(telegram_id=telegram_id, user_name=user_name)
        user.save()
    except peewee.IntegrityError:
        pass


def check_id(telegram_id):
    all_users = all_users_id()
    if telegram_id in all_users:
        return True
    else:
        return False


# print message for all users
def all_users_id():
    users_id_list = []
    all_users = Users.select()
    for user in all_users:
        users_id_list.append(user.telegram_id)
    return users_id_list


def get_language(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    return user.language


# user_language = 'RU' or 'KZ'
def edit_language(telegram_id, user_language):
    user = Users.get(Users.telegram_id == telegram_id)
    user.language = user_language
    user.save()


def get_user_questions_available(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    count = user.questions_available
    return count


def reduce_user_questions_available(telegram_id):
    query = Users.update(questions_available=Users.questions_available - 1).where(Users.telegram_id == telegram_id)
    query.execute()


def up_user_questions_available(telegram_id):
    query = Users.update(questions_available=100000).where(Users.telegram_id == telegram_id)
    query.execute()


def up_admin_questions_available():
    query = Users.update(questions_available=5).where(Users.telegram_id == ADMIN_ID)
    query.execute()


def get_time_visit(telegram_id):
    user = Users.get(Users.telegram_id == telegram_id)
    return user.last_visit


def update_time_visit(telegram_id):
    query = Users.update(last_visit=datetime.now()).where(Users.telegram_id == telegram_id)
    query.execute()


def get_loser_list():
    two_week_ago = datetime.now().date() - timedelta(days=14)
    loser_list = []
    all_users = Users.select()
    for user in all_users:
        questions_available = user.questions_available
        last_visit = user.last_visit.date()
        if questions_available == 0 and last_visit < two_week_ago:
            loser_list.append(user.telegram_id)
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


def set_new_promo_code(school_name, promo_code, secret_key, bank_account, agree):
    new_promo_code = PromoCodes(school_name=school_name,
                                promo_code=promo_code,
                                secret_key=secret_key,
                                bank_account=bank_account,
                                agree=agree)
    new_promo_code.save()


def get_number_of_references(promo_code):
    promo_code = PromoCodes.get(PromoCodes.promo_code == promo_code)
    number_of_references = promo_code.number_of_references
    return number_of_references


def get_percent(promo_code):
    promo_code = PromoCodes.get(PromoCodes.promo_code == promo_code)
    percent = promo_code.percent
    return percent


def get_bank_account(promo_code):
    promo_code = PromoCodes.get(PromoCodes.promo_code == promo_code)
    bank_account = promo_code.bank_account
    return bank_account


def up_number_of_references(promo_code):
    query = PromoCodes.update(number_of_references=PromoCodes.number_of_references + 1).where(
        PromoCodes.promo_code == promo_code)
    query.execute()


def check_super_promo_code():
    try:
        promo_code = SuperPromoCode.get(SuperPromoCode.id == 1)
        return promo_code.promo_code
    except:
        return False


def up_number_of_references_super():
    query = SuperPromoCode.update(number_of_references=SuperPromoCode.number_of_references + 1).where(
        SuperPromoCode.id == 1)
    query.execute()


def set_default_super_promo_code():
    if check_super_promo_code():
        delete_super_promo_code()
    promo_code = SuperPromoCode()
    promo_code.save()


def delete_super_promo_code():
    promo_code = SuperPromoCode.delete().where(SuperPromoCode.id == 1)
    promo_code.execute()


def edit_super_promo_code(name):
    query = SuperPromoCode.update(promo_code=name).where(SuperPromoCode.id == 1)
    query.execute()


def get_agreement_school_list():
    school_list = []
    promo_codes = PromoCodes.select().where(PromoCodes.agree == 1).order_by(PromoCodes.number_of_references.desc())
    for promo_code in promo_codes:
        school = f'{promo_code.school_name} = {promo_code.number_of_references}'
        school_list.append(school)
    return school_list


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


def view_number_of_users():
    all_users = Users.select()
    number_of_users = len(all_users)
    return number_of_users


def view_number_of_users_on_day():
    today = datetime.now().date()
    all_users = Users.select().where(Users.registration_date == today)
    number_of_users = len(all_users)
    return number_of_users


def view_number_of_users_on_week():
    old_day = datetime.now().date() - timedelta(days=7)
    all_users = Users.select().where(Users.registration_date > old_day)
    number_of_users = len(all_users)
    return number_of_users


def view_number_of_users_on_month():
    this_month = datetime.now().month
    this_year = datetime.now().year
    users_count = 0
    all_users = Users.select()
    for user in all_users:
        if user.registration_date.year == this_year and user.registration_date.month == this_month:
            users_count += 1
    return users_count


def view_number_of_users_on_year():
    this_year = datetime.now().year
    users_count = 0
    all_users = Users.select()
    for user in all_users:
        if user.registration_date.year == this_year:
            users_count += 1
    return users_count


def view_users_online_now():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month and user.last_visit.hour == today.hour:
            count += 1
    return count


def view_users_online_today():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month and user.last_visit.day == today.day:
            count += 1
    return count


def view_users_online_on_this_week():
    old_day = datetime.now() - timedelta(days=7)
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.date() > old_day.date():
            count += 1
    return count


def view_users_online_on_this_month():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year and user.last_visit.month == today.month:
            count += 1
    return count


def view_users_online_on_this_year():
    today = datetime.now()
    count = 0
    all_users = Users.select()
    for user in all_users:
        if user.last_visit.year == today.year:
            count += 1
    return count


def view_all_users_list():
    result = []
    all_users = Users.select()
    result.append('id' + ' ' * 20 + 'имя' + ' ' * 20 + 'count')
    for user in all_users:
        result.append(f"{user.telegram_id} {user.user_name} {user.questions_available}")
    return '\n'.join(result)


def view_number_of_promo_codes():
    all_promo_codes = PromoCodes.select()
    number_of_promo_codes = len(all_promo_codes)
    return number_of_promo_codes


def view_number_of_promo_codes_on_day():
    today = datetime.now().date()
    all_promo_codes = PromoCodes.select().where(PromoCodes.registration_date == today)
    number_of_promo_codes = len(all_promo_codes)
    return number_of_promo_codes


def view_number_of_promo_codes_on_week():
    old_day = datetime.now().date() - timedelta(days=7)
    all_promo_codes = PromoCodes.select().where(PromoCodes.registration_date > old_day)
    number_of_promo_codes = len(all_promo_codes)
    return number_of_promo_codes


def view_number_of_promo_codes_on_month():
    this_month = datetime.now().month
    this_year = datetime.now().year
    promo_codes_count = 0
    all_promo_codes = PromoCodes.select()
    for promo_code in all_promo_codes:
        if promo_code.registration_date.year == this_year and promo_code.registration_date.month == this_month:
            promo_codes_count += 1
    return promo_codes_count


def view_number_of_promo_codes_on_year():
    this_year = datetime.now().year
    promo_codes_count = 0
    all_promo_codes = PromoCodes.select()
    for promo_code in all_promo_codes:
        if promo_code.registration_date.year == this_year:
            promo_codes_count += 1
    return promo_codes_count


def view_all_promo_code_list():
    result = []
    all_promo_codes = PromoCodes.select().order_by(PromoCodes.number_of_references.desc())
    result.append('школа > промо-код > упоминаний')
    for promo_code in all_promo_codes:
        result.append(f"{promo_code.school_name} {promo_code.promo_code} {promo_code.number_of_references}")
    return '\n'.join(result)


def view_number_of_payed_users():
    payed_users = Users.select().where(Users.questions_available > QUESTION_AVAILABLE)
    payed_users_count = len(payed_users)
    return payed_users_count


def get_conversion():
    users = view_number_of_users()
    payed_users = view_number_of_payed_users()
    try:
        conversion = payed_users * 100 / users
    except ZeroDivisionError:
        conversion = 0
    return payed_users, conversion


def view_percent_of_language_choice():
    users = view_number_of_users()
    ru_language = 0
    kz_language = 0
    all_users = Users.select()
    for user in all_users:
        if user.language == 'RU':
            ru_language += 1
        else:
            kz_language += 1
    result_ru = ru_language * 100 / users
    result_kz = kz_language * 100 / users
    return result_ru, result_kz


def get_big_statistics():
    users = view_number_of_users()
    users_today = view_number_of_users_on_day()
    users_on_week = view_number_of_users_on_week()
    users_on_month = view_number_of_users_on_month()
    users_on_year = view_number_of_users_on_year()

    users_online = view_users_online_now()
    users_online_today = view_users_online_today()
    users_online_on_this_week = view_users_online_on_this_week()
    users_online_on_this_month = view_users_online_on_this_month()
    users_online_on_this_year = view_users_online_on_this_year()

    super_promo_code = check_super_promo_code()

    promo_codes = view_number_of_promo_codes()
    promo_codes_today = view_number_of_promo_codes_on_day()
    promo_codes_on_week = view_number_of_promo_codes_on_week()
    promo_codes_on_month = view_number_of_promo_codes_on_month()
    promo_codes_on_year = view_number_of_promo_codes_on_year()

    payed_users, conversion = get_conversion()
    ru_users, kz_users = view_percent_of_language_choice()

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
        '\n',
        f'Супер промокод: {super_promo_code}',
        '\n'
        f'Зарегистрировано промо-кодов: {promo_codes}',
        f'Зарегистрировано промо-кодов сегодня: {promo_codes_today}',
        f'Зарегистрировано промо-кодов на этой неделе: {promo_codes_on_week}',
        f'Зарегистрировано промо-кодов в этом месяце: {promo_codes_on_month}',
        f'Зарегистрировано промо-кодов за год: {promo_codes_on_year}',
        f'',
        f'Оплатили сервис: {payed_users} пользователей',
        f'Конверсия: {conversion}%',
        f'',
        f'Русскоязычных пользователей: {ru_users}%',
        f'Казахоязычных пользователей: {kz_users}%'
    ]

    return '\n'.join(text)


if __name__ == '__main__':
    create_new_tables(table_names)
    set_default_super_promo_code()
    for el in get_all_ru_questions():
        print(el, end=',\n')
