import os
import json
from dotenv import load_dotenv

load_dotenv()

DEBUG = json.loads(os.getenv('DEBUG').lower())

TEST_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_ADDRESS = os.getenv('BOT_ADDRESS')
BOT_NAME = os.getenv('BOT_NAME')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

BASE_PRICE = int(os.getenv('BASE_PRICE'))
PRICE_AFTER_14DAYS = int(os.getenv('PRICE_AFTER_14DAYS'))
PRICE_AFTER_45DAYS = int(os.getenv('PRICE_AFTER_45DAYS'))

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

pay_config = {
    'KASSA_24_LOGIN_RU': os.getenv('KASSA_24_LOGIN_RU'),
    'KASSA_24_PASSWORD_RU': os.getenv('KASSA_24_PASSWORD_RU'),
    'KASSA_24_LOGIN_KZ': os.getenv('KASSA_24_LOGIN_KZ'),
    'KASSA_24_PASSWORD_KZ': os.getenv('KASSA_24_PASSWORD_KZ')
}


db_config = {
    'db_name': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER_NAME,
    'password': DB_PASSWORD
}
