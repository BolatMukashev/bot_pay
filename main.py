from flask import Flask, url_for, request, render_template, send_from_directory
from werkzeug.utils import redirect
from db_operation import *
from gmail import send_emails_to_schools
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
                    sub_title = 'Промокод изменен!'
                    html = you_promo_code_registered_message(new_promo_code)
                    send_emails_to_schools(emails, sub_title, html)
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


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/accept_page', methods=['GET', 'POST'])
def set_accept():
    """telegram_id - int
    для проверки, сохраняем файл с id в папке backup сайта:
    file_name = os.path.join(os.getcwd(), 'backup', 'pay_data.json')
    create_new_json_file(file_name, telegram_id)
    """
    telegram_id = request.json['metadata']['telegram_id']
    up_user_time_limit_days(telegram_id, 365)
    update_user_made_payment_status(telegram_id)
    res = json.dumps({"accepted": True})
    return res


if __name__ == '__main__':
    app.run()
