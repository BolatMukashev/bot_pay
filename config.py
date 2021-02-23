import os
import json
from dotenv import load_dotenv

load_dotenv()

DEBUG = json.loads(os.getenv('DEBUG').lower())
TEST_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_ADDRESS = os.getenv('BOT_ADDRESS')
BOT_NAME = os.getenv('BOT_NAME')
PAY_SITE_ADDRESS = os.getenv('PAY_SITE_ADDRESS')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
BASE_PRICE = int(os.getenv('BASE_PRICE'))
PRICE_AFTER_14DAYS = int(os.getenv('PRICE_AFTER_14DAYS'))
PRICE_AFTER_45DAYS = int(os.getenv('PRICE_AFTER_45DAYS'))
APP_USER_NAME = os.getenv('APP_USER_NAME')
APP_PASSWORD = os.getenv('APP_PASSWORD')
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GMAIL_WINDOWS_PASSWORD = os.getenv('GMAIL_WINDOWS_PASSWORD')
GMAIL_LINUX_PASSWORD = os.getenv('GMAIL_LINUX_PASSWORD')


db_config = {
    'db_name': 'pdd_bot',
    'user': 'root',
    'password': DB_PASSWORD,
    'host': 'localhost',
}
