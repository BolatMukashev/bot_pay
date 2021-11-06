import pymysql
from peewee import *
from peewee import InternalError
from config import DB_CONFIGS
from datetime import datetime, timedelta, date


conn = pymysql.connect(host=DB_CONFIGS['host'],
                       port=DB_CONFIGS['port'],
                       user=DB_CONFIGS['user'],
                       password=DB_CONFIGS['password'])


db = MySQLDatabase(DB_CONFIGS['db_name'],
                   host=DB_CONFIGS['host'],
                   port=DB_CONFIGS['port'],
                   user=DB_CONFIGS['user'],
                   password=DB_CONFIGS['password'])


def create_database(db_name: str) -> None:
    """
    Создаем новую базу
    :param db_name: Имя базы
    :return:
    """
    try:
        conn.cursor().execute(f'create database {db_name}')
        print('База данных успешно создана...')
    except pymysql.err.ProgrammingError:
        print('База данных уже была создана ранее...')


def create_new_tables(db_models):
    """Создаем новую таблицу в базе"""
    try:
        db.connect()
    except InternalError as err:
        print(str(err))
    else:
        db.create_tables(db_models)
        print('Таблицы созданы...')
    finally:
        db.close()


def database_initialization():
    """Инициализация базы. Закрыват открытое соединение с базой. Если явно не закрывать - будут проблемы с MySQL"""
    if not db.is_closed():
        db.close()


def plus_one_day() -> datetime:
    """
    :return: Текущая дата + 1 день
    """
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow


def get_date() -> date:
    today = datetime.now().date()
    return today


class BaseModel(Model):
    class Meta:
        database = db  # соединение с базой, из шаблона выше


# удалить second_week_promotional_offer, sixth_week_promotional_offer, made_payment
class User(BaseModel):
    """Пользователь"""
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False, unique=True)
    full_name = CharField(null=True, max_length=300)
    country = CharField(null=False, default='RU')
    language = CharField(null=False, default='RU')
    registration_date = DateTimeField(default=datetime.now)
    registration_is_over = BooleanField(null=False, default=False)
    time_limit = DateTimeField(default=plus_one_day)
    last_visit = DateTimeField(default=datetime.now)
    promo_code_used = BooleanField(null=False, default=False)
    price_in_rubles = IntegerField(null=False)
    referral = IntegerField(null=True)
    tariff = CharField(null=False, max_length=50, default='basic')

    class Meta:
        db_table = "users"


class Leaver(BaseModel):
    """Ливер"""
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False, unique=True)
    tariff = CharField(null=False, max_length=50)
    referral = IntegerField(null=True)
    full_name = CharField(null=True, max_length=300)

    class Meta:
        db_table = "leavers"


class PayOrder(BaseModel):
    """Платёж"""
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False)
    date = DateTimeField(default=datetime.now)
    order_number = IntegerField(null=False, unique=True)
    price = IntegerField(null=False)

    class Meta:
        db_table = "pay_orders"


class PromoCode(BaseModel):
    """Промокод регистрация"""
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False, unique=True)
    date = DateTimeField(default=datetime.now)
    promo_code = CharField(null=False)

    class Meta:
        db_table = "promo_code_used_history"


class AutoSchool(BaseModel):
    """Автошкола"""
    id = PrimaryKeyField(null=False)
    school_name = CharField(null=False, max_length=100)
    country = CharField(null=False, max_length=100)
    city = CharField(null=False, max_length=100)
    phones = BlobField(null=True, default=None)
    emails = BlobField(null=True, default=None)
    instagram = CharField(null=True, max_length=100, default=None)
    registration_date = DateField(default=get_date)
    secret_key = CharField(null=False, max_length=100, unique=True)
    promo_code = CharField(null=False, max_length=100, unique=True)
    number_of_references = IntegerField(null=False, default=0)
    notified = BooleanField(null=False, default=False)

    class Meta:
        db_table = "auto_schools"


class QuestionRU(BaseModel):
    """Вопросы на русском"""
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_ru"


class QuestionKZ(BaseModel):
    """Вопросы на казахском"""
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_kz"


table_names = [User, QuestionRU, QuestionKZ, AutoSchool, PayOrder, PromoCode, Leaver]

__all__ = ['IntegrityError', 'User', 'PayOrder', 'PromoCode', 'QuestionRU', 'QuestionKZ', 'AutoSchool', 'Leaver',
           'create_new_tables', 'create_database', 'database_initialization', 'table_names']
