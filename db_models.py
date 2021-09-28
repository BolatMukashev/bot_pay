import pymysql
from peewee import *
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


class BaseModel(Model):
    class Meta:
        database = db  # соединение с базой, из шаблона выше


# удалить second_week_promotional_offer, sixth_week_promotional_offer
class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram_id = IntegerField(null=False, unique=True)
    full_name = CharField(null=True, max_length=300)
    country = CharField(null=False, default='RU')
    language = CharField(null=False, default='RU')
    registration_date = DateTimeField(default=datetime.now())
    # import datetime
    # import pytz
    # print(datetime.datetime.now())
    # then = datetime.datetime.now(pytz.utc)
    # print(then)
    # print(then.astimezone(pytz.timezone('Asia/Atyrau')))
    registration_is_over = BooleanField(null=False, default=False)
    time_limit = DateTimeField(default=datetime.now() + timedelta(days=1))
    last_visit = DateTimeField(default=datetime.now())
    promo_code_used = BooleanField(null=False, default=False)
    price_in_rubles = IntegerField(null=False)
    made_payment = BooleanField(null=False, default=False)
    second_week_promotional_offer = BooleanField(null=False, default=False)
    sixth_week_promotional_offer = BooleanField(null=False, default=False)

    class Meta:
        db_table = "users"


class AutoSchools(BaseModel):
    id = PrimaryKeyField(null=False)
    school_name = CharField(null=False, max_length=100)
    country = CharField(null=False, max_length=100)
    city = CharField(null=False, max_length=100)
    phones = BlobField(null=False)
    emails = BlobField(null=False)
    registration_date = DateTimeField(default=datetime.now().date())
    secret_key = CharField(null=False, max_length=100, unique=True)
    promo_code = CharField(null=False, max_length=100, unique=True)
    number_of_references = IntegerField(null=False, default=0)
    notified = BooleanField(null=False, default=False)

    class Meta:
        db_table = "auto_schools"


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
