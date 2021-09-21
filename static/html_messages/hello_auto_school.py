def hello_auto_school_message(secret_key):
    html = ["""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Приветствую</title>
        <style type="text/css">
            /*Псевдо-Обнуление*/
            *,
            *:before,
            *:after {
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                box-sizing: border-box;
            }

            :focus,
            :active {
                outline: none;
            }

            a:focus,
            a:active {
                outline: none;
            }

            nav,
            footer,
            header,
            aside {
                display: block;
            }

            input,
            button,
            textarea {
                font-family: inherit;
            }

            input::-ms-clear {
                display: none;
            }

            button {
                cursor: pointer;
            }

            button::-moz-focus-inner {
                padding: 0;
                border: 0;
            }

            a,
            a:visited {
                text-decoration: none;
            }

            a:hover {
                text-decoration: none;
            }

            ul li {
                list-style: none;
            }

            img {
                vertical-align: top;
            }

            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button {
                -webkit-appearance: none;
            }

            /*--------------------*/
            .main__block {
                width: 100%;
                height: 100%;
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

            .block__secret {
                color: rgb(136, 0, 91);
                font-weight: 800;
            }

            .secret {
                color: rgb(255, 0, 85);
                font-size: 1.2em;
            }

            .button {
                width: 280px;
                height: 60px;
                background-color: darkblue;
                color: white;
                font-size: 16px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                letter-spacing: 1.5px;
                font-weight: 800;
                border: 2px solid white;
                border-radius: 30px;
            }
        </style>
    </head>
    """,
            f"""
    <body>
        <div class="main__block">
            <h1>Новая образовательная платорма</h1>
            <h2>на базе мессенджера Telegram (<a href="https://t.me/pdd_good_bot" target="_blank">@pdd_good_bot</a>)
            </h2>
            <p>Мы хотим дать студентам Автошкол новые возможности в обучении.</p>
            <p>Используя современные технологии, мы создали продукт,<br>
            который обеспечивает привычный пользовательский опыт.<br>
                А что может быть более привычным для современного человека, как не мессенджеры,<br>
                которыми он каждый день пользуется?</p>
            <p>Наша платформа, это дополнительный удобный инструмент в обучении правилам вождения.</p>
            <p>Мы не конкурируем с книгами по вождению, или инструкторами.<br>Мы гармонично их дополняем!</p>
            <p class='block__secret'>Ваш секретный ключ:<br><span class="secret">{secret_key}</span></p>
            <p>Используйте его, чтобы активировать <b>Ваш</b> Промокод на нашем сайте:</p>
            <div><a href="https://pddgoodbot.ru"><button class="button">Активировать Промокод</button></a></div>
            <h3>Что даёт ПРОМОКОД?</h3>
            <p>Дополнительные <b>5 дней</b> доступа к нашей Образовательной платформе для <b>ВСЕХ</b>,<br>
                кто воспользуется вашим Промокодом и <b>50% скидка</b> на покупку годового доступа.</p>
        </div>
    </body>
    """]
    html_message = ''.join(html)
    return html_message
