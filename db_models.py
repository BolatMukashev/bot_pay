from peewee import *
import pymysql
from config import db_config, MY_BANK_ACCOUNT, PERCENT, QUESTION_AVAILABLE
from datetime import datetime


db = MySQLDatabase(db_config['db_name'],
                   user=db_config['user'],
                   password=db_config['password'],
                   host=db_config['host'])


class BaseModel(Model):
    class Meta:
        database = db  # соединение с базой, из шаблона выше


class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    registration_date = DateTimeField(default=datetime.now().date())
    telegram_id = CharField(null=False, max_length=100, unique=True)
    user_name = CharField(null=False, max_length=200)
    questions_available = IntegerField(null=False, default=QUESTION_AVAILABLE)
    language = CharField(null=False, max_length=100, default='RU')
    last_visit = DateTimeField(default=datetime.now())

    class Meta:
        db_table = "users"


class PromoCodes(BaseModel):
    id = PrimaryKeyField(null=False)
    registration_date = DateTimeField(default=datetime.now().date())
    school_name = CharField(null=False, max_length=100)
    promo_code = CharField(null=False, max_length=100, unique=True)
    secret_key = CharField(null=False, max_length=100)
    bank_account = CharField(null=False, max_length=100)
    percent = IntegerField(null=False, default=PERCENT)
    number_of_references = IntegerField(null=False, default=0)
    agree = BooleanField(null=False)

    class Meta:
        db_table = "promo_codes"


# СуперПромоКод - для юзеров, с count = 0, с давней датой регистрации больше 1-3 месяцев.
# Скидка 75% = 250тг, но оплата лично мне. С ограничением по времени 3-5 дней.


class SuperPromoCode(BaseModel):
    id = CharField(null=False, default=1)
    promo_code = CharField(null=False, max_length=100, default='THE_BEST_PROGRAM')
    bank_account = CharField(null=False, max_length=100, default=MY_BANK_ACCOUNT)
    percent = IntegerField(null=False, default=100)
    number_of_references = IntegerField(null=False, default=0)

    class Meta:
        primary_key = False
        db_table = "super_promo_code"


class QuestionsRU(BaseModel):
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_ru"


class QuestionsKZ(BaseModel):
    id = PrimaryKeyField(null=False)
    question = TextField(null=False)
    correct_answer = TextField(null=False)
    all_answers = BlobField(null=False)
    explanation = TextField(default=None, null=True)
    image_code = TextField(default=None, null=True)

    class Meta:
        db_table = "questions_kz"


# счетчик для подсчета вопросов в Вопросах. Решил не использовать.
class Info(BaseModel):
    id = PrimaryKeyField(null=False)
    number_of_questions = IntegerField(null=False)

    class Meta:
        db_table = "info"
