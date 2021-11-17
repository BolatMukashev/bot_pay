import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG')))

TEST_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_NAME = os.getenv('BOT_NAME')
BOT_ADDRESS = os.getenv('BOT_ADDRESS')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

BASE_PRICE = int(os.getenv('BASE_PRICE'))                               # delete
PRICE_AFTER_20DAYS = int(os.getenv('PRICE_AFTER_20DAYS'))               # delete

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

GMAIL = os.getenv('GMAIL')

RUBLES_EXCHANGE_RATE = 6.04

TARIFFS = {
    'basic':  {"daily_limit": 5, "price": 0},
    'premium':  {"daily_limit": 30, "price": 150},
    'premium_max': {"daily_limit": 999, "price": 300}
}

REFERRAL_BONUS_VALUE = 5

DONATE_URL = 'https://ecommerce.pult24.kz/invoice?id=12916339944358246'     # изменить на ioka

KASSA_24_PAY_CONFIGS = {
    'KASSA_24_LOGIN_RU': os.getenv('KASSA_24_LOGIN_RU'),
    'KASSA_24_PASSWORD_RU': os.getenv('KASSA_24_PASSWORD_RU'),
    'KASSA_24_LOGIN_KZ': os.getenv('KASSA_24_LOGIN_KZ'),
    'KASSA_24_PASSWORD_KZ': os.getenv('KASSA_24_PASSWORD_KZ')
}

IOKA_PAY_CONFIGS = {
    'IOKA_TEST_KEY': os.getenv('IOKA_TEST_KEY'),
    'IOKA_SECRET_KEY': os.getenv('IOKA_SECRET_KEY'),
    'IOKA_PUBLIC_KEY': os.getenv('IOKA_PUBLIC_KEY')
}


DB_CONFIGS = {
    'db_name': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER_NAME,
    'password': DB_PASSWORD
}

CACHE = {
    'number_of_questions_in_RU_db': None,
    'number_of_questions_in_KZ_db': None
}

users_data_cache = {}
