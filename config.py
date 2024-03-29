import os
from dotenv import load_dotenv

load_dotenv()

EVENT = bool(int(os.getenv('EVENT')))

RUBLES_EXCHANGE_RATE = 6                # ruble/tenge

TARIFFS = {
    'basic':  {"daily_limit": 5, "price": 0, 'translate': 'Базовый'},
    'premium':  {"daily_limit": 30, "price": 200, 'translate': 'Премиум'},
    'premium_max': {"daily_limit": 999, "price": 300, 'translate': 'Премиум Max'}
}

REFERRAL_BONUS_VALUE = 5

DONATE_URL = 'https://ecommerce.pult24.kz/invoice?id=12916339944358246'     # изменить на ioka

DEBUG = bool(int(os.getenv('DEBUG')))

TEST_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_NAME = os.getenv('BOT_NAME')
BOT_ADDRESS = os.getenv('BOT_ADDRESS')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

APP_USER_NAME = os.getenv('APP_USER_NAME')
APP_PASSWORD = os.getenv('APP_PASSWORD')

SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GMAIL_WINDOWS_PASSWORD = os.getenv('GMAIL_WINDOWS_PASSWORD')
GMAIL_LINUX_PASSWORD = os.getenv('GMAIL_LINUX_PASSWORD')

DB_NAME = os.getenv('DB_NAME')
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_PASSWORD = os.getenv('DB_PASSWORD')

PG_DB_NAME = os.getenv('PG_DB_NAME')
PG_DB_USER_NAME = os.getenv('PG_DB_USER_NAME')
PG_DB_HOST = os.getenv('PG_DB_HOST')
PG_DB_PORT = int(os.getenv('PG_DB_PORT'))
PG_DB_PASSWORD = os.getenv('PG_DB_PASSWORD')

GMAIL = os.getenv('GMAIL')

KASSA_24_PAY_CONFIGS = {
    'KASSA_24_LOGIN_RU': os.getenv('KASSA_24_LOGIN_RU'),
    'KASSA_24_PASSWORD_RU': os.getenv('KASSA_24_PASSWORD_RU'),
    'KASSA_24_LOGIN_KZ': os.getenv('KASSA_24_LOGIN_KZ'),
    'KASSA_24_PASSWORD_KZ': os.getenv('KASSA_24_PASSWORD_KZ')
}

IOKA_PAY_CONFIGS = {
    'IOKA_TEST_KEY': os.getenv('IOKA_TEST_KEY'),
    'IOKA_SECRET_KEY': os.getenv('IOKA_SECRET_KEY'),
    'IOKA_PUBLIC_KEY': os.getenv('IOKA_PUBLIC_KEY'),
    'IOKA_API_KEY': os.getenv('IOKA_API_KEY')
}


MYSQL_DB_CONFIGS = {
    'db_name': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER_NAME,
    'password': DB_PASSWORD
}

POSTGRESQL_DB_CONFIGS = {
    'db_name': PG_DB_NAME,
    'host': PG_DB_HOST,
    'port': PG_DB_PORT,
    'user': PG_DB_USER_NAME,
    'password': PG_DB_PASSWORD
}

CACHE = {
    'number_of_questions_in_RU_db': None,
    'number_of_questions_in_KZ_db': None
}

users_data_cache = {}
