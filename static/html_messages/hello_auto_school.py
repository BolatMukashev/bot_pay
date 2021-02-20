def hello_auto_school_message(secret_key):
    html = ["""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Заглавие работает?</title>
        <style type="text/css">
            
            .main__block {
                padding: 20px;
                text-align: center;
            }
            h1 {
                font-family: Verdana, Arial, Helvetica, sans-serif;
                font-size: 1.5em;
                color: #333366;
            }
            h2 {
                font-family: Verdana, Arial, Helvetica, sans-serif;
                font-size: 1.2em;
                color: #333366;
            }
            p {
                font-family: Verdana, Arial, Helvetica, sans-serif;
                font-size: 1em;
                color: rgb(29, 24, 24);
            }
            .secret {
                color: rgb(116, 0, 106);
            }
        </style>
    </head>
    """,
            f"""
    <body>
        <div class="main__block">
            <h1>Новая образовательная платорма</h1>
            <h2>на базе мессенджера Telegram (@pdd_good_bot)</h2>
            <p>Мы делаем мир лучше</p>
            <p>Ваш секретный ключ:</p>
            <p class="secret">{secret_key}</p>
            <p>Используйте его, чтобы активировать Промокод на нашем сайте</p>
            <p>Тут будет кнопка</p>
            <h3>Что даёт ПРОМОКОД?</h3>
            <p>Дополнительные 7 дней доступа к Образовательной платформе</p>
            <p>50% скидку на покупку годового доступа</p>
            <p><img src="https://avatarko.ru/img/kartinka/33/multfilm_lyagushka_32117.jpg" alt="Письма мастера дзен"></p>
        </div>
    </body>
    """]
    html_message = ''.join(html)
    return html_message
