MESSAGE = dict(start_admin_text="""
Показать статистику:
/statistics
Узнать о пользователе:
/get_user_info

MESSAGES
Отправить картинку + подпись (рус):
/send_post_ru
Отправить картинку + подпись (каз):
/send_post_kz
Отправить картинку + подпись (ru):
/send_post_russia
Отправить картинку + подпись (kz):
/send_post_kazakhstan

EMAIL
Отправить приветственное сообщениe:
/send_hello_emails_to_new_schools
Отправить email всем Автошколам:
/send_email_for_all_auto_schools

ACTIONS
+3 минуты админу:
/up_admin_time_limit
+3 дня использования всем!
/up_time_limit_for_all_at_days_03
+30 дней использования всем!
/up_time_limit_for_all_at_days_30
50% скидка лузерам
/set_50_percent_price_for_losers
Удалить Автошколу из базы:
/delete_auto_school
Бэкап данных:
/backup_all_data
Установить команды:
/set_commands
""",
               start_user_text='Добро пожаловать <b>{}</b>!\n'
                               'У вас есть <b>24 часа</b> чтобы ознакомится с нашей Образовательной платформой',
               language_choice='Выберите язык\n'
                               '------------------------\n'
                               'Тілді таңдаңыз',
               language_set_ok_RU='Язык изменён ✓',
               language_set_ok_KZ='Тіл өзгерді ✓',
               country_choice_RU='Из какой Вы страны?',
               country_choice_KZ='Сіз қай елденсіз?',
               country_edited_ok_RU='Страна выбрана ✓',
               country_edited_ok_KZ='Ел таңдалды ✓',
               registration_ok_RU='Регистрация прошла успешно!\nНажми кнопку <b>СТАРТ</b>',
               registration_ok_KZ='Тіркеу сәтті аяқталды!\n<b>СТАРТ</b> батырмасын басыңыз',
               info_RU='Telegram налагает ограничения на количество символов в тексте при составлении опросов '
                       'и викторин.\n'
                       'Поэтому некоторые слова в ответах были заменены на более короткие аналоги, например:\n'
                       '<i>транспорное средство -> транспорт -> авто -> ТС</i>\n'
                       'А конструкции вида <i>дом/дорога/машина</i> - означают:\n'
                       '<i>дом или дорога или машина</i>',
               info_KZ='Telegram сауалнамалар мен викториналар құрғанда мәтіндегі таңбалар санына шектеулер қояды.\n'
                       'Сондықтан жауаптардағы кейбір сөздер қысқа аналогтармен ауыстырылды.'
                       'Мысалы, <i>көлік құралы -> көлік</i>',
               limit_error_RU="Просим прощения, но Ваш пробный период закончился\n\n"
                              "Способы продлить доступ:\n\n"
                              "/pay - купить годовой доступ\n\n"
                              "/promo_code - активировать промокод\n\n"
                              "/promotions - акции и скидки\n\n",
               limit_error_KZ='Кешіріңіз, бірақ сіздің сынақ мерзіміңіз аяқталды\n\n'
                              'Қол жеткізуді кеңейту жолдары:\n\n'
                              '/pay - жыл сайынғы рұқсатты сатып алу\n\n'
                              '/promo_code - промокодты қолданыңыз\n\n'
                              '/promotions - жеңілдіктер мен акциялар\n\n',
               pay_message_RU='Получите ГОД безлемитного доступа к нашей образовательной платформе.\n'
                              'Для Вас это будет стоить всего {} {}! {}\n'
                              '<i>Ссылка на оплату будет активна 20 минут</i>',
               pay_message_KZ='Біздің білім беру платформасына БIР ЖЫЛ шектеусіз қол жеткізіңіз.\n'
                              'Сіз үшін бұл бар болғаны {} {}! {}\n'
                              '<i>Төлем сілтемесі 20 минут бойы белсенді болады</i>',
               pay_registered_message_RU='Ваш платёж принят\n'
                                         'Номер платежа: {}\n'
                                         'Чтобы продолжить обучение нажмите /question',
               pay_registered_message_KZ='Сіздің төлеміңіз қабылданды\n'
                                         'Төлем нөмірі: {}\n'
                                         'Оқуды жалғастыру үшін /question басыңыз',
               bot_link_RU='Вернуться к боту',
               bot_link_KZ='Ботқа оралу',
               link_to_chat_RU='Обсудить вопросы 👉🏻 https://t.me/pdd_forum',
               link_to_chat_KZ='Сұрақтарды талқылау 👉🏻 https://t.me/pdd_forum',
               link_error_chat_RU='Сообщить об ошибке 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy',
               link_error_chat_KZ='Қате туралы хабарлау 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy')

PROMO_CODE = {
    'registered': 'Данный промокод уже зарегистрирован',
    'error': 'Промокод введен не верно',
    'promo_code_error_RU': 'Промокод не найден',
    'promo_code_error_KZ': 'Промокод табылмады',
    'promo_code_none_text_RU': 'Не использовался',
    'promo_code_none_text_KZ': 'Қолданылмаған',
    'promo_code_command_text_RU': 'Активируй промокод и получи +5 дней безлимитного доступа к нашей образовательной '
                                  'платформе.\n'
                                  'А ещё ты получишь 50% скидку на покупку годового доступа!\n'
                                  'Введи промокод:',
    'promo_code_command_text_KZ': 'Промокод жазып, біздің білім беру платформасына +5 күндік шектеусіз қол жеткізіңіз.'
                                  '\n'
                                  'Сіз сондай-ақ жылдық қол жетімділікті сатып алғанда 50% жеңілдікке ие боласыз!\n'
                                  'Промокодты жаз:',
    'promo_code_was_used_RU': 'Промокод уже был использован Вами ранее',
    'promo_code_was_used_KZ': 'Промокодты сіз бұрын қолданғансыз',
    'promo_code_activated_RU': 'Поздравляю! Промокод активирован 🎉 \nЧтобы продолжить обучение нажмите /question',
    'promo_code_activated_KZ': 'Құттықтаймыз! Промокод белсендірілді 🎉 \nОқуды жалғастыру үшін /question басыңыз'
}

OFFERS = {
    'second_week_promotional_offer_RU': 'Здравствуй. Тебе доступна 50%-ная скидка на покупку годового доступа в нашей '
                                        'образовательной платформе.\nОбязательно воспользуйся!\n'
                                        'Для оплаты нажми /pay\n\n'
                                        'Чтобы продолжить обучение после оплаты нажмите на /question',
    'second_week_promotional_offer_KZ': 'Сәлем. Біздің білім беру платформасына бір жылдық қол жетімділікті сатып алу '
                                        'үшін сізде 50% жеңілдік бар.\nПайдалануды ұмытпаңыз\n'
                                        'Төлем жасау үшін /pay басыңыз\n\n'
                                        'Төлемнен кейін оқытуды жалғастыру үшін /question басыңыз',
    'sixth_week_promotional_offer_RU': 'Здравствуй. Последняя возможность!\n'
                                       'Тебе доступна скидка в 75% на покупку '
                                       'годового доступа в нашей образовательной платформе.\n'
                                       'Обязательно воспользуйся!\n'
                                       'Для оплаты нажми /pay\n\n'
                                       'Чтобы продолжить обучение после оплаты нажмите на /question',
    'sixth_week_promotional_offer_KZ': 'Сәлем. Соңғы мүмкіндік!\n'
                                       'Біздің білім беру платформасына бір жылдық қол '
                                       'жетімділікті сатып алу кезінде 75% жеңілдік бар.\n'
                                       'Пайдалануды ұмытпаңыз!\n'
                                       'Төлем жасау үшін /pay басыңыз\n\n'
                                       'Төлемнен кейін оқытуды жалғастыру үшін /question басыңыз',
}

PROMOTIONS = {
    '100friends_RU': 'Акция! Приведи друга и получи +1 день бесплатного доступа к боту!',
    '100friends_KZ': 'Қор! Досыңызға хабарласыңыз және ботқа +1 күн тегін кіру мүмкіндігін алыңыз!',
    '100friends_action_message1_RU': '⬇️ Вот твоя ссылка! Отправляй её друзьям ⬇️',
    '100friends_action_message2_RU': 'Бот поможет:\n'
                                     '🔹 Подготовится к экзамену на знание ПДД\n'
                                     '🔹 Закрепить полученные в автошколе знания\n'
                                     '🔹 Узнать размеры штрафов за нарушения ПДД',
    '100friends_action_message1_KZ': '⬇️ Міне сілтеме! Достарыңызға жіберіңіз ⬇️',
    '100friends_action_message2_KZ': 'Бот көмектеседі:\n'
                                     '🔹 Жол қозғалысы ережелерін білу бойынша емтиханға дайындалуға\n'
                                     '🔹 Автомектепте алған білімдерін бекіту\n'
                                     '🔹 Жол қозғалысы ережелерін бұзғаны үшін салынатын айыппұл көлемін анықтауға'
}

GIFT_CERTIFICATE = {
    'identification_error_RU': 'Ошибка! Невозможно идентифицировать пользователя!\n'
                               'Возможно, данные пользователя скрыты настройками приватности',
    'identification_error_KZ': 'Қате! Пайдаланушыны анықтау мүмкін емес!\n'
                               'Мүмкін пайдаланушы деректері құпиялылық параметрлері арқылы жасырылған',
}

BUTTONS = {
    'lang_RU': '🇷🇺 Русский язык',
    'lang_KZ': '🇰🇿 Қазақ тілі',
    'next_RU': 'Далее ❯❯❯',
    'back_RU': '❮❮❮ Назад',
    'next_KZ': 'Келесі ❯❯❯',
    'back_KZ': '❮❮❮ Кері',
    'start': 'СТАРТ',
    'russia': '🇷🇺 РОССИЯ',
    'kazakhstan': '🇰🇿 қазақстан',
    'pay_RU': 'Оплатить',
    'pay_KZ': 'Төлеу',
    'do_it_RU': 'Участвовать',
    'do_it_KZ': 'Қатысу'
}

COMMANDS_DESCRIPTIONS = {
    'ALL': {
        'question': 'Новый вопрос. Жаңа сұрақ',
        'penalty': 'Посмотреть штрафы. Айыппұлдарды қарау',
        'pay': 'Оплатить. Төлеу',
        'promo_code': 'Использовать промокод. Промокодты қолдану',
        'promotions': 'Акции и скидки. Қор мен жеңілдіктер',
        'chat': 'Обсудить вопросы. Сұрақтарды талқылау',
        'error': 'Сообщить об ошибке. Қате туралы хабарлау',
        'language': 'Изменить язык. Тілді өзгерту',
        'country': 'Изменить страну. Ел өзгерту',
        'info': 'Подсказки. Кеңестер',
        'language_code': ''
    },
    'RU': {
        'question': 'Новый вопрос',
        'penalty': 'Посмотреть штрафы',
        'pay': 'Оплатить',
        'promo_code': 'Использовать промокод',
        'promotions': 'Акции и скидки',
        'chat': 'Обсудить вопросы',
        'error': 'Сообщить об ошибке',
        'language': 'Изменить язык',
        'country': 'Изменить страну',
        'info': 'Подсказки',
        'language_code': 'ru'
    },
    'KZ': {
        'question': 'Жаңа сұрақ',
        'penalty': 'Айыппұлдарды қарау',
        'pay': 'Төлеу',
        'promo_code': 'Промокодты қолдану',
        'promotions': 'Қор мен жеңілдіктер',
        'chat': 'Сұрақтарды талқылау',
        'error': 'Қате туралы хабарлау',
        'language': 'Тілді өзгерту',
        'country': 'Ел өзгерту',
        'info': 'Кеңестер',
        'language_code': 'kk'
    }
}

STICKERS = {
    'hello': 'CAACAgIAAxkBAAEB1rxgGo2hRDlaGoiEHOZf3mY6C19jKQACKwIAArnzlwv7BQOMjG9ozB4E',
    'repair': 'CAACAgIAAxkBAAEB1rhgGo2MKy7iUaRUUGj5b1LO4V0sHgACMQEAArnzlws-7wljOEZF0x4E',
    'message': 'CAACAgIAAxkBAAEB1rpgGo2RcuS-bNqr3URmqOIh9Nv3SAACPAEAArnzlwvMnvUK9IcNFR4E',
    'come_back': 'CAACAgIAAxkBAAEB1sRgGpJtzbzRtNodSiGctvngZ9AccQACHwEAArnzlwu5r6hVbS11sB4E',
    'all_good': 'CAACAgIAAxkBAAEB1sJgGpJkbNi5ocJafzCeo8OUd7b_VQACJgEAArnzlwt4WnW4BxSuMB4E',
    'flower': 'CAACAgIAAxkBAAEDBDZhWy9yYcsn6eTkTp1-Yvm79of3zwACZAEAArnzlwvMmCtHVcQbbiEE',
    'NO': 'CAACAgIAAxkBAAEB3HtgIV_xw819XJj4oKtFyPqCyh_pxwACawEAArnzlwslqyJF_izS0h4E'
}

IMAGES = {
    '100friends': 'AgACAgIAAxkBAAI9mmDhhtWeuMCQ_jCRRgABOuH3RU2X_gACZ7QxGxJDEEv-BXPviTTuPwEAAwIAA3MAAyAE',
    '50percent': 'AgACAgIAAxkBAAJJ_mFKJUPa3raFEIrcXN52xQMdQwrhAALvtjEbECJQSrt4_xDHMSCrAQADAgADcwADIQQ',
    'test_img': 'AgACAgIAAxkBAAIVFWFKKS30e59wdOZts8xDlTnYxVBQAALItDEbc-dZSszgkrm9TU6sAQADAgADcwADIQQ'
}
