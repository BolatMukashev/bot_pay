from peewee import *
import pymysql
from config import db_config
from datetime import datetime, timedelta


db = MySQLDatabase(db_config['db_name'],
                   user=db_config['user'],
                   password=db_config['password'],
                   host=db_config['host'])


class BaseModel(Model):
    class Meta:
        database = db  # соединение с базой, из шаблона выше


class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram_id = CharField(null=False, max_length=100, unique=True)
    full_name = CharField(null=True, max_length=200)
    country = CharField(null=False, max_length=100, default='RU')
    language = CharField(null=False, max_length=100, default='RU')
    registration_date = DateTimeField(default=datetime.now().date())
    last_visit = DateTimeField(default=datetime.now())
    time_limit = DateTimeField(default=datetime.now() + timedelta(days=1))
    promo_code_used = BooleanField(null=False, default=False)
    made_payment = BooleanField(null=False, default=False)

    class Meta:
        db_table = "users"


class PromoCodes(BaseModel):
    id = PrimaryKeyField(null=False)
    school_name = CharField(null=False, max_length=100)
    secret_key = CharField(null=False, max_length=100, unique=True)
    registration_date = DateTimeField(default=datetime.now().date())
    promo_code = CharField(null=False, max_length=100, unique=True)
    number_of_references = IntegerField(null=False, default=0)

    class Meta:
        db_table = "promo_codes"


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
