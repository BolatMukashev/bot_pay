import pymysql
from peewee import *
from peewee import InternalError
from config import DB_CONFIGS
from datetime import datetime, timedelta


conn = pymysql.connect(host=DB_CONFIGS['host'],
                       port=DB_CONFIGS['port'],
                       user=DB_CONFIGS['user'],
                       password=DB_CONFIGS['password'])


db = MySQLDatabase(DB_CONFIGS['db_name'],
                   host=DB_CONFIGS['host'],
                   port=DB_CONFIGS['port'],
                   user=DB_CONFIGS['user'],
                   password=DB_CONFIGS['password'])


def create_database(db_name):
    try:
        conn.cursor().execute(f'create database {db_name}')
        print('База данных успешно создана...')
    except pymysql.err.ProgrammingError:
        print('База данных уже была создана ранее...')


def create_new_tables(db_models):
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
    if not db.is_closed():
        db.close()


def plus_one_day() -> object:
    """
    :return: Текущая дата + 1 день
    """
    date = datetime.now() + timedelta(days=1)
    return date


def get_date() -> object:
    date = datetime.now().date()
    return date


class BaseModel(Model):
    class Meta:
        database = db  # соединение с базой, из шаблона выше


# удалить second_week_promotional_offer, sixth_week_promotional_offer, made_payment
class User(BaseModel):
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
    made_payment = BooleanField(null=False, default=False)
    second_week_promotional_offer = BooleanField(null=False, default=False)
    sixth_week_promotional_offer = BooleanField(null=False, default=False)

    class Meta:
        db_table = "users"


class PayOrder(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False)
    date = DateTimeField(default=datetime.now)
    order_number = IntegerField(null=False, unique=True)
    price = IntegerField(null=False)

    class Meta:
        db_table = "pay_orders"


class AutoSchool(BaseModel):
    id = PrimaryKeyField(null=False)
    school_name = CharField(null=False, max_length=100)
    country = CharField(null=False, max_length=100)
    city = CharField(null=False, max_length=100)
    phones = BlobField(null=False)
    emails = BlobField(null=False)
    registration_date = DateTimeField(default=get_date)
    secret_key = CharField(null=False, max_length=100, unique=True)
    promo_code = CharField(null=False, max_length=100, unique=True)
    number_of_references = IntegerField(null=False, default=0)
    notified = BooleanField(null=False, default=False)

    class Meta:
        db_table = "auto_schools"


class QuestionRU(BaseModel):
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_ru"


class QuestionKZ(BaseModel):
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_kz"


table_names = [User, QuestionRU, QuestionKZ, AutoSchool, PayOrder]

__all__ = ['IntegrityError', 'User', 'PayOrder', 'QuestionRU', 'QuestionKZ', 'AutoSchool', 'create_new_tables',
           'create_database', 'database_initialization', 'table_names']
