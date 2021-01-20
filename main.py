import os
from flask import Flask, url_for, request, render_template, send_from_directory, make_response, session
from werkzeug.utils import redirect
from werkzeug.exceptions import BadRequestKeyError
from config import *
from db_operation import set_new_promo_code, check_promo_code, up_number_of_references, up_user_questions_available, \
    check_super_promo_code, up_number_of_references_super, uppercase_check
from messages import MESSAGE

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=SESSION_SECRET_KEY,
    USERNAME=APP_USER_NAME,
    PASSWORD=APP_PASSWORD
))


path = os.path.dirname(os.path.abspath(__file__))
path_to_documents = os.path.join(path, 'documents')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/promo_code', methods=['GET', 'POST'])
def promo_code():
    if request.method == 'POST':
        school_name = request.form["school_name"]
        user_promo_code = request.form["promo_code"]
        secret_code = request.form["secret_code"]
        bank_account = request.form["bank_account"]
        try:
            agree = bool(request.form["agree"])
        except BadRequestKeyError:
            agree = False
        if uppercase_check(user_promo_code):
            if not check_promo_code(user_promo_code):
                set_new_promo_code(school_name, user_promo_code, secret_code, bank_account, agree)
                return redirect(url_for('promo_code_registered', user_promo_code=user_promo_code))
            else:
                error_text = 'Данный промокод уже зарегистрирован'
                return render_template('promo_code.html', error_text=error_text, school_name=school_name,
                                       secret_code=secret_code, bank_account=bank_account)
        else:
            error_text = 'Промокод введен не верно'
            return render_template('promo_code.html', error_text=error_text, school_name=school_name,
                                   secret_code=secret_code, bank_account=bank_account)
    else:
        return render_template('promo_code.html')


@app.route('/offer')
def offer():
    return send_from_directory(directory=path_to_documents,
                               filename='offer.pdf',
                               mimetype='application/pdf')


@app.route('/promo_code_registered')
def promo_code_registered():
    user_promo_code = request.args["user_promo_code"]
    return render_template('promo_code_registered.html', BOT_ADDRESS=BOT_ADDRESS, user_promo_code=user_promo_code)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        telegram_id = request.form["telegram_id"]
        user_name = request.form["user_name"]
        language = request.form["language"]
        if language == 'KZ':
            pay_registered_message = MESSAGE['pay_registered_message_kz']
            promo_code_error = MESSAGE['promo_code_error_kz']
            bot_link = MESSAGE['bot_link_kz']
            pay_page = 'pay_kz.html'
        else:
            pay_registered_message = MESSAGE['pay_registered_message_ru']
            promo_code_error = MESSAGE['promo_code_error_ru']
            bot_link = MESSAGE['bot_link_ru']
            pay_page = 'pay_ru.html'

        user_promo_code = request.form["discount"]

        if user_promo_code:
            if check_promo_code(user_promo_code):
                resp = make_response(redirect(url_for('pay_operation', language=language)))
                resp.set_cookie('telegram_id', telegram_id)
                resp.set_cookie('user_name', user_name)
                resp.set_cookie('language', language)
                resp.set_cookie('promo_code_used', user_promo_code)
                session['price'] = str(PRICE_WITH_PROMO_CODE)
                return resp
            elif user_promo_code == check_super_promo_code():
                resp = make_response(redirect(url_for('pay_operation', language=language)))
                resp.set_cookie('telegram_id', telegram_id)
                resp.set_cookie('user_name', user_name)
                resp.set_cookie('language', language)
                resp.set_cookie('promo_code_used', user_promo_code)
                session['price'] = str(PRICE_WITH_SUPER_PROMO_CODE)
                return resp
            else:
                error_text = user_promo_code + ' ' + promo_code_error
                return render_template(pay_page, error_text=error_text, bot_name=BOT_NAME,
                                       bot_address=BOT_ADDRESS, telegram_id=telegram_id, user_name=user_name,
                                       price=PRICE)
        else:
            # up_user_questions_available(telegram_id)
            # 'Без промокода. 100% оплата'
            resp = make_response(redirect(url_for('pay_operation', language=language)))
            resp.set_cookie('telegram_id', telegram_id)
            resp.set_cookie('user_name', user_name)
            resp.set_cookie('language', language)
            session['price'] = str(PRICE)
            return resp
    else:
        try:
            telegram_id = request.args["telegram_id"]
            user_name = request.args["user_name"].replace('_', ' ')
            language = request.args["language"]
            if language == 'KZ':
                pay_page = 'pay_kz.html'
            else:
                pay_page = 'pay_ru.html'
            return render_template(pay_page, bot_name=BOT_NAME, bot_address=BOT_ADDRESS, telegram_id=telegram_id,
                                   user_name=user_name, price=PRICE)
        except BadRequestKeyError:
            return redirect(url_for('pay_error'))


# resp = make_response(render_template('pay_ru.html', bot_name=BOT_NAME, bot_address=BOT_ADDRESS,
#                                      telegram_id=telegram_id, user_name=user_name, price=PRICE))
# resp.set_cookie('price', '200')
# resp.set_cookie('telegram_id', telegram_id)
# return resp


@app.route('/pay_instructions')
def pay_instructions():
    return send_from_directory(directory=path_to_documents,
                               filename='pay_instructions.pdf',
                               mimetype='application/pdf')


@app.route('/confidence_politics')
def confidence_politics():
    return send_from_directory(directory=path_to_documents,
                               filename='confidence_politics.pdf',
                               mimetype='application/pdf')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/pay_operation/<language>')
def pay_operation(language):
    telegram_id = request.cookies.get('telegram_id') or None
    user_name = request.cookies.get('user_name') or None
    language = request.cookies.get('language') or 'RU'
    promo_code_used = request.cookies.get('promo_code_used') or None
    price = session.get('price') or None
    if telegram_id:
        if language == 'KZ':
            page = 'pay_operation_kz.html'
        else:
            page = 'pay_operation_ru.html'
        return render_template(page, bot_name=BOT_NAME, bot_address=BOT_ADDRESS,
                               telegram_id=telegram_id, user_name=user_name, language=language, price=price,
                               promo_code=promo_code_used)
    else:
        return redirect(url_for('pay_error'))


@app.route('/pay_error')
def pay_error():
    return render_template('pay_error.html', BOT_ADDRESS=BOT_ADDRESS, message=MESSAGE['pay_error_message'])


if __name__ == '__main__':
    app.run()
