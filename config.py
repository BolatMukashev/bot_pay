import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_ADDRESS = os.getenv('BOT_ADDRESS')
BOT_NAME = os.getenv('BOT_NAME')
PAY_SITE_ADDRESS = os.getenv('PAY_SITE_ADDRESS')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
PRICE = int(os.getenv('PRICE'))
PRICE_WITH_PROMO_CODE = int(os.getenv('PRICE_WITH_PROMO_CODE'))
PRICE_WITH_SUPER_PROMO_CODE = int(os.getenv('PRICE_WITH_SUPER_PROMO_CODE'))
QUESTION_AVAILABLE = int(os.getenv('QUESTION_AVAILABLE'))
PERCENT = int(os.getenv('PERCENT'))
MY_BANK_ACCOUNT = os.getenv('MY_BANK_ACCOUNT')
APP_USER_NAME = os.getenv('APP_USER_NAME')
APP_PASSWORD = os.getenv('APP_PASSWORD')
SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')

db_config = {
    'db_name': 'pdd_bot',
    'user': 'root',
    'password': DB_PASSWORD,
    'host': 'localhost',
}
