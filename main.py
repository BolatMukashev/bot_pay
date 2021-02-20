import os
from flask import Flask, url_for, request, render_template, send_from_directory, make_response
from werkzeug.utils import redirect
from werkzeug.exceptions import BadRequestKeyError
import config
from db_operation import *
from gmail import send_emails_to_schools
from messages import MESSAGE
from static.html_messages.you_promo_code_registered import you_promo_code_registered_message

app = Flask(__name__)

app.config.update(dict(
    DEBUG=config.DEBUG,
    SECRET_KEY=config.SESSION_SECRET_KEY,
    USERNAME=config.APP_USER_NAME,
    PASSWORD=config.APP_PASSWORD
))


path = os.path.dirname(os.path.abspath(__file__))
path_to_documents = os.path.join(path, 'documents')


@app.route('/')
def index():
    return render_template('index.html', bot_address=config.BOT_ADDRESS)


@app.route('/promo_code', methods=['GET', 'POST'])
def promo_code():
    if request.method == 'POST':
        secret_key = request.form['secret_key']
        new_promo_code = request.form['promo_code'].upper()
        if check_secret_key(secret_key):
            if not check_promo_code(new_promo_code):
                if promo_code_check_to_correct(new_promo_code):
                    edit_promo_code(secret_key, new_promo_code)
                    emails = get_auto_school_emails_by(secret_key)
                    title = 'PDD GOOD BOT'
                    sub_title = 'Промокод изменен!'
                    html = you_promo_code_registered_message(new_promo_code)
                    my_message = 'Прочти обязательно!'
                    send_emails_to_schools(emails, title, sub_title, html, my_message)
                    return redirect(url_for('promo_code_registered', new_promo_code=new_promo_code))
                else:
                    promo_code_error = 'Только английские символы'
                    return render_template('promo_code.html', secret_key=secret_key, promo_code_error=promo_code_error)
            else:
                promo_code_error = 'Этот ПРОМОКОД зянят. Попробуйте другой.'
                return render_template('promo_code.html', secret_key=secret_key, promo_code_error=promo_code_error)
        else:
            secret_key_error = 'Секретный ключ не найден'
            return render_template('promo_code.html', secret_key_error=secret_key_error)
    else:
        return render_template('promo_code.html')


@app.route('/offer')
def offer():
    return send_from_directory(directory=path_to_documents,
                               filename='offer.pdf',
                               mimetype='application/pdf')


@app.route('/promo_code_registered/<new_promo_code>')
def promo_code_registered(new_promo_code):
    return render_template('promo_code_registered.html', BOT_ADDRESS=config.BOT_ADDRESS, new_promo_code=new_promo_code)


@app.route('/pay')
def pay():
    try:
        telegram_id = request.args["telegram_id"]
        user_name = get_user_name_by(telegram_id)
        user_language = get_user_language(telegram_id)
        user_country = get_user_country(telegram_id)
        price = get_finally_price(telegram_id)
        monetary_unit = get_monetary_unit_by_user_country(telegram_id)
        secret_key = config.SESSION_SECRET_KEY
    except BadRequestKeyError:
        telegram_id = 'undefiled'
        user_name = 'undefiled'
        user_language = 'RU'
        user_country = 'RU'
        price = config.BASE_PRICE
        monetary_unit = 'рублей'
        secret_key = None

    return render_template('pay.html', bot_name=config.BOT_NAME, bot_address=config.BOT_ADDRESS, price=price,
                           user_language=user_language, telegram_id=telegram_id, user_name=user_name,
                           user_country=user_country, monetary_unit=monetary_unit, secret_key=secret_key)


@app.route('/confidence_and_pay')
def confidence_and_pay():
    return send_from_directory(directory=path_to_documents,
                               filename='confidence_and_pay.pdf',
                               mimetype='application/pdf')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/accept')
def accept():
    try:
        secret_key = request.args["secret_key"]
        telegram_id = request.args["telegram_id"]
    except BadRequestKeyError:
        return 'Bad'
    if secret_key != config.SESSION_SECRET_KEY:
        return 'Bad'
    up_user_time_limit_1years(telegram_id)
    update_user_made_payment_status(telegram_id)
    return 'All good!'


@app.route('/pay_registered/<language>')
def pay_registered(language):
    button_text = MESSAGE[f'bot_link_{language}']
    message = MESSAGE[f'pay_registered_message_{language}']
    return render_template('pay_registered.html', BOT_ADDRESS=config.BOT_ADDRESS,
                           message=message, button_text=button_text)


if __name__ == '__main__':
    app.run()
