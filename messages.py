"""
Применение адаптации языка, пример:
pay_message_RU_RU - где:
первая RU - страна, вторая RU - язык
"""

MESSAGE = dict(start_user_text='Добро пожаловать <b>{}</b>!\n',
               language_choice='Выберите язык\n'
                               '------------------------\n'
                               'Тілді таңдаңыз',
               language_set_ok_RU='Язык изменён ✓',
               language_set_ok_KZ='Тіл өзгерді ✓',
               country_choice_RU='Из какой Вы страны?',
               country_choice_KZ='Сіз қай елденсіз?',
               country_edited_ok_RU='Страна выбрана ✓',
               country_edited_ok_KZ='Ел таңдалды ✓',
               registration_ok_RU='Регистрация прошла успешно!\n'
                                  'Ваш тариф: <b>{}</b>\n'
                                  'Количество доступных вопросов в день: <b>{}</b>\n'
                                  'У вас есть нелимитированных <b>{}</b> чтобы ознакомится с нашей Образовательной '
                                  'платформой\n'
                                  'Нажми кнопку <b>СТАРТ</b>',
               registration_ok_KZ='Тіркеу сәтті аяқталды!\n'
                                  'Сіздің тарифіңіз: <b>{}</b>\n'
                                  'Күніне қолжетімді сұрақтар саны: <b>{}</b>\n'
                                  'Біздің білім беру платформасын тексеру үшін сізде шексіз <b>{}</b> бар\n'
                                  '<b>СТАРТ</b> батырмасын басыңыз',
               tariff_RU='Ваш тариф: <b>{}</b>\n'
                         'Количество доступных вопросов в день: <b>{}</b>\n'
                         'Из них использовано сегодня: <b>{}</b>\n\n'
                         'Увеличить количество доступных за день вопросов до 30 ➝ приобрети тариф '
                         '<b>\"Премиум\"</b>\n\n'
                         'Или пользуйся нашим сервисом без ограничений ➝ приобрети тариф <b>\"Премиум Max\"</b>',
               tariff_KZ='Сіздің тарифіңіз: <b>{}</b>\n'
                         'Күніне қолжетімді сұрақтар саны: <b>{}</b>\n'
                         'Оның бүгінгі күні қолданылған: <b>{}</b>\n\n'
                         'Күніне қолжетімді сұрақтар санын 30-ға дейін арттыру үшін ➝ <b>\"Премиум\"</b> тарифті '
                         'сатып ал\n\n'
                         'Ал біздің қызметімізді шектеусіз пайдалану үшін ➝ <b>\"Премиум Max\"</b> тарифті сатып ал',
               info_RU='Telegram налагает ограничения на количество символов в тексте при составлении опросов '
                       'и викторин.\n'
                       'Поэтому некоторые слова в ответах были заменены на более короткие аналоги, например:\n'
                       '<i>транспорное средство -> транспорт -> авто -> ТС</i>\n'
                       'А конструкции вида <i>дом/дорога/машина</i> - означают:\n'
                       '<i>дом или дорога или машина</i>',
               info_KZ='Telegram сауалнамалар мен викториналар құрғанда мәтіндегі таңбалар санына шектеулер қояды.\n'
                       'Сондықтан жауаптардағы кейбір сөздер қысқа аналогтармен ауыстырылды.'
                       'Мысалы, <i>көлік құралы -> көлік</i>',
               limit_error_RU="Просим прощения, но Ваш дневной лимит закончился\n\n"
                              "<i>Автоматическое пополнение дневного лимита произойдет в 00:00 по времени "
                              "Москвы</i>\n\n"
                              "Доступны следующие способы увеличить дневной лимит:\n\n"
                              "/pay - купить премиум доступ\n\n"
                              "/promo_code - активировать промокод\n\n"
                              "/promotions - акции и скидки\n\n",
               limit_error_KZ='Кешіріңіз, бірақ сіздің күнделікті шектеуіңіз аяқталды.\n\n'
                              '<i>Тәуліктік лимитті автоматты түрде толтыру Нұр-Сұлтан уақыты бойынша сағат 02:00-де '
                              'болады</i>\n\n '
                              'Күнделікті шектеуді арттыру үшін келесі әдістер қол жетімді:\n\n'
                              '/pay - премиум қолжетімділікті сатып алу\n\n'
                              '/promo_code - промокодты қолдану\n\n'
                              '/promotions - жеңілдіктер мен акциялар\n\n',
               bot_link_RU='Вернуться к боту',
               bot_link_KZ='Ботқа оралу',
               link_to_chat_RU='Обсудить вопросы 👉🏻 https://t.me/pdd_forum',
               link_to_chat_KZ='Сұрақтарды талқылау 👉🏻 https://t.me/pdd_forum',
               link_error_chat_RU='Сообщить об ошибке 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy',
               link_error_chat_KZ='Қате туралы хабарлау 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy',
               function_error_RU='Функция находиться в разработке...',
               function_error_KZ='Функция әзірленуде...',
               cancel_action_RU='Действие отменено',
               cancel_action_KZ='Әрекеттен бас тартылды',
               attraction_text_RU='Вы привели друга! Ваш дневной лимит увеличен на +5 вопросов',
               attraction_text_KZ='Сіз дос әкелдіңіз! Сіздің күнделікті лимитіңіз +5 сұраққа ұлғайтылды'
               )

PAY = dict(message_RU_RU='Подключение тарифа <b>\"{tariff}\"</b>\n'
                         'Для Вас это будет стоить всего <b>{price_ruble}</b> рублей! (<i>{price_tenge}</i> ₸)\n'
                         'Срок действия тарифа неограничен\n'
                         '<i>Ссылка на оплату будет активна 20 минут</i>',
           message_RU_KZ='<b>\"{tariff}\"</b> тарифіне қосылу\n'
                         'Бұл сізге бар болғаны <b>{price_ruble}</b> рубльді құрайды! (<i>{price_tenge}</i> ₸)\n'
                         'Тарифтің әрекет ету мерзімі шектеусіз\n'
                         '<i>Төлем сілтемесі 20 минут бойы белсенді болады</i>',
           message_KZ_RU='Подключение тарифа <b>\"{tariff}\"</b>\n'
                         'Для Вас это будет стоить всего <b>{price_tenge}</b> тенге!\n'
                         'Срок действия тарифа неограничен\n'
                         '<i>Ссылка на оплату будет активна 20 минут</i>',
           message_KZ_KZ='<b>\"{tariff}\"</b> тарифіне қосылу\n'
                         'Бұл сізге бар болғаны <b>{price_tenge}</b> тенге құрайды!\n'
                         'Тарифтің әрекет ету мерзімі шектеусіз\n'
                         '<i>Төлем сілтемесі 20 минут бойы белсенді болады</i>',
           pay_registered_message_RU='Ваш платёж принят\n'
                                     'Номер платежа: {}',
           pay_registered_message_KZ='Сіздің төлеміңіз қабылданды\n'
                                     'Төлем нөмірі: {}'
           )

PROMO_CODE = {
    'registered': 'Данный промокод уже зарегистрирован',
    'error': 'Промокод введен не верно',
    'promo_code_error_RU': 'Промокод не найден',
    'promo_code_error_KZ': 'Промокод табылмады',
    'promo_code_none_text_RU': 'Не использовался',
    'promo_code_none_text_KZ': 'Қолданылмаған',
    'promo_code_command_text_RU': 'Активируй промокод и получи 50% скидку на покупку тарифов <b>Премиум</b> и '
                                  '<b>Премиум Max</b>!\n'
                                  'Введи промокод:',
    'promo_code_command_text_KZ': 'Промокодты іске қосыңыз және <b>Премиум</b> және <b>Премиум Max</b> жоспарларын '
                                  'сатып алуға 50% жеңілдік алыңыз!\n'
                                  'Промокодты жаз:',
    'promo_code_was_used_RU': 'Промокод уже был использован Вами ранее',
    'promo_code_was_used_KZ': 'Промокодты сіз бұрын қолданғансыз',
    'promo_code_activated_RU': 'Поздравляю! Промокод активирован 🎉',
    'promo_code_activated_KZ': 'Құттықтаймыз! Промокод белсендірілді 🎉'
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
    '100friends_RU': 'Акция! Приводи друзей и увеличивай дневной лимит на +5 вопросов за каждого приведенного друга!',
    '100friends_KZ': 'Қор! Достарыңызды ұсыныңыз және әр жолдаған досыңызға күнделікті шектеуді +5 сұраққа көбейтіңіз!',
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

ROADMAP = {
    'roadmap_text_RU': "Мы довольно молодая компания (на рынке с 2021 года), но у нас большие амбиции!\n"
                       "Наши дальнейшие планы по улучшению платформы:\n\n"
                       "🎯 Добавить подарочные сертификаты - пользователи смогут покупать и дарить своим родным и "
                       "близким сертификаты на обучение на нашей платформе\n\n"
                       "🎯 Добавить статистику обучения (графики, показатели) - это позволит пользователям отслеживать "
                       "свой прогресс\n\n"
                       "🎯 Геймифицировать процесс обучения (таблица рейтингов, ранги) - это позволит пользователям "
                       "дольше оставаться на платформе и интереснее проводить время\n\n"
                       "🎯 Перерисовать изображения в обновленном формате. Большая часть изображений морально "
                       "устарела\n\n"
                       "🎯 Добавить поддержку языков всех стран ближнего зарубежья - тем самым расширив аудиторию и "
                       "обеспечить еще большее удобство для пользователей\n\n"
                       "🎯 Добавить больше подсказок к вопросам, с разборами тех или иных моментов\n\n\n",
    'roadmap_text_KZ': "Біз өте жас компаниямыз (2021 жылдан бастап нарықта), бірақ бізде үлкен амбициялар бар!\n"
                       "Платформаны жақсарту бойынша біздің болашақ жоспарларымыз:\n\n"
                       "🎯 Сыйлық сертификаттарын қосу - пайдаланушылар біздің платформада оқыту үшін отбасы мен "
                       "достарына сертификаттарды сатып алып, бере алады\n\n"
                       "🎯 Оқу статистикасын қосу (графиктер, көрсеткіштер) - бұл пайдаланушыларға олардың үлгерімін "
                       "бақылауға мүмкіндік береді\n\n"
                       "🎯 Оқу процесін геймификациялау (рейтингтер кестесі, дәрежелер) - бұл пайдаланушыларға "
                       "платформада ұзағырақ қалуға және қызықты уақыт өткізуге мүмкіндік береді\n\n"
                       "🎯 Суреттерді жаңартылған форматта қайта сызу. Кескіндердің көпшілігі ескірген\n\n"
                       "🎯 Барлық көрші елдердің тілдеріне қолдау қосу - осылайша аудиторияны кеңейтіп, "
                       "пайдаланушылар үшін одан да үлкен ыңғайлылықты қамтамасыз етеді\n\n"
                       "🎯 Белгілі бір тармақтарды талдау арқылы сұрақтарға қосымша кеңестер қосу\n\n\n"
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
    'do_it_KZ': 'Қатысу',
    'help_project_RU': 'Помочь проекту',
    'help_project_KZ': 'Жобаға көмектесу',
    'cancel_RU': 'Отмена',
    'cancel_KZ': 'Жою',
    'get_question_RU': 'Продолжить обучение',
    'get_question_KZ': 'Оқуды жалғастыру',
    'pay_premium_RU': 'Подключить \"Премиум\"',
    'pay_premium_KZ': '\"Премиум\" тарифті қосу',
    'pay_premium_max_RU': 'Подключить \"Премиум Max\"',
    'pay_premium_max_KZ': '\"Премиум Max\" тарифті қосу'
}

COMMANDS_DESCRIPTIONS = {
    'ALL': {
        'question': 'Новый вопрос. Жаңа сұрақ',
        'penalty': 'Посмотреть штрафы. Айыппұлдарды қарау',
        'tariffs': 'Тарифы. Тарифтер',
        'promo_code': 'Использовать промокод. Промокодты қолдану',
        'promotions': 'Акции и скидки. Қор мен жеңілдіктер',
        'certificate': 'Подарочный сертификат. Сыйлық сертификаты',
        'roadmap': 'Карта развития. Жобаны дамыту картасы',
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
        'tariffs': 'Тарифы',
        'promo_code': 'Использовать промокод',
        'promotions': 'Акции и скидки',
        'certificate': 'Подарочный сертификат',
        'roadmap': 'Карта развития проекта',
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
        'tariffs': 'Тарифтер',
        'promo_code': 'Промокодты қолдану',
        'promotions': 'Қор мен жеңілдіктер',
        'certificate': 'Сыйлық сертификаты',
        'roadmap': 'Жобаны дамыту картасы',
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
    '100friends_RU': 'AgACAgIAAxkBAAI9mmDhhtWeuMCQ_jCRRgABOuH3RU2X_gACZ7QxGxJDEEv-BXPviTTuPwEAAwIAA3MAAyAE',
    '100friends_KZ': 'AgACAgIAAxkBAAKMRmGbRphFkjoLjOHt8Zzt_vSMrPvsAAJftjEb0W3ZSDyZvIujlqDhAQADAgADcwADIgQ',
    'roadmap_RU': 'AgACAgIAAxkBAAKF0mGXLBPO7sopnYejS6XKGQJeUCs-AAIKujEbniq5SNIaG13bvwZkAQADAgADcwADIgQ',
    'roadmap_KZ': 'AgACAgIAAxkBAAKF1GGXLBu0WJGgE8V1IAlBpgU45WUxAAILujEbniq5SBOVJwvzqUe-AQADAgADcwADIgQ',
    'tariffs_RU_RU': 'AgACAgIAAxkBAAKFzGGXK_DcXrgeiOHE6CRWrDlXFyejAAIGujEbniq5SH28EwQ1zHpCAQADAgADcwADIgQ',
    'tariffs_RU_KZ': 'AgACAgIAAxkBAAKFzGGXK_DcXrgeiOHE6CRWrDlXFyejAAIGujEbniq5SH28EwQ1zHpCAQADAgADcwADIgQ',
    'tariffs_KZ_RU': 'AgACAgIAAxkBAAKFzmGXK_vMqBZm6QdZ9t19Zc8h85_DAAIIujEbniq5SJ3IY3R6OuKmAQADAgADcwADIgQ',
    'tariffs_KZ_KZ': 'AgACAgIAAxkBAAKF0GGXLAABVz_-27a210gM9Qqz6pgCZwACCboxG54quUhHoUfXR7_y_wEAAwIAA3MAAyIE',
    'tariffs_RU_RU_event': 'AgACAgIAAxkBAAKN2WGdzx4sp7jTlZj7KAxpKO5KtlvsAAIYvDEbq6vwSIuno0S4YFEgAQADAgADcwADIgQ',
    'tariffs_RU_KZ_event': 'AgACAgIAAxkBAAKN2WGdzx4sp7jTlZj7KAxpKO5KtlvsAAIYvDEbq6vwSIuno0S4YFEgAQADAgADcwADIgQ',
    'tariffs_KZ_RU_event': 'AgACAgIAAxkBAAKN22GdzzSizPcgpT1P9BfcuPBbuTU0AAIZvDEbq6vwSN0qQh8LlN79AQADAgADcwADIgQ',
    'tariffs_KZ_KZ_event': 'AgACAgIAAxkBAAKN3WGdzz5HC77KceODAicEFLjs5fU-AAIavDEbq6vwSOg2s77wQcFRAQADAgADcwADIgQ',
    'tariff_premium_RU': 'AgACAgIAAxkBAAKM-WGcj1FFBLAysUILlOrJxKcb_O1iAAJXtjEbNQTgSOjprFyKnbvcAQADAgADcwADIgQ',
    'tariff_premium_KZ': 'AgACAgIAAxkBAAKM-2Gcj1jgaZNNGRa6WVGYafNt0jH6AAJYtjEbNQTgSCQtDEeSh8VSAQADAgADcwADIgQ',
    'tariff_premium_max_RU': 'AgACAgIAAxkBAAKM_WGcj15wyYtiTbr1rCZzUWatSCDoAAJZtjEbNQTgSFpE4bqigQpvAQADAgADcwADIgQ',
    'tariff_premium_max_KZ': 'AgACAgIAAxkBAAKM_2Gcj2MbzavNEjlvrtINC0FOd0_BAAJatjEbNQTgSNFaaP9CK0v7AQADAgADcwADIgQ'
}

TEST_IMAGES = {
    '100friends_RU': 'AgACAgIAAxkBAAIbomGXlmjmzsCaL29LeYwt3Pr0sh8UAALAtzEbBAABuEh_usx4iwhVCQEAAwIAA3MAAyIE',
    '100friends_KZ': 'AgACAgIAAxkBAAIbyGGbSICxWKUk81KoQuXZRdHZEt0OAAJftjEb0W3ZSPdERC5IlxFqAQADAgADcwADIgQ',
    'roadmap_RU': 'AgACAgIAAxkBAAIbpGGXlnrkCmlbUqevR5FexrpmHvqgAAIKujEbniq5SCTbK5SFPK4rAQADAgADcwADIgQ',
    'roadmap_KZ': 'AgACAgIAAxkBAAIbpmGXloDxY0bz0MTMMxfaT-EuGcBKAAILujEbniq5SJazTwABG0EYUwEAAwIAA3MAAyIE',
    'tariffs_RU_RU': 'AgACAgIAAxkBAAIbXmGXg7mppaX3k7u6YgwW7hY6GyAYAAIGujEbniq5SDRAdtiyqIS0AQADAgADcwADIgQ',
    'tariffs_RU_KZ': 'AgACAgIAAxkBAAIb_2GbcIkLRNLtoOJLMEwTXtdj-GcDAAKRtjEbwBjYSCTKGxX-S9nfAQADAgADcwADIgQ',
    'tariffs_KZ_RU': 'AgACAgIAAxkBAAIbYGGXhAVWvQvsdnYFK8-SXOPvw22kAAIIujEbniq5SMTOERv_GzxbAQADAgADcwADIgQ',
    'tariffs_KZ_KZ': 'AgACAgIAAxkBAAIbYmGXhBz2lgjytEbbMxGyIx8frIU2AAIJujEbniq5SNU4JRvd2wABmAEAAwIAA3MAAyIE',
    'tariffs_RU_RU_event': 'AgACAgIAAxkBAAIc12Gd0RGyuYl32TfyJRvCGJI-eYFIAAIYvDEbq6vwSAWXwbvepGrFAQADAgADcwADIgQ',
    'tariffs_RU_KZ_event': 'AgACAgIAAxkBAAIc12Gd0RGyuYl32TfyJRvCGJI-eYFIAAIYvDEbq6vwSAWXwbvepGrFAQADAgADcwADIgQ',
    'tariffs_KZ_RU_event': 'AgACAgIAAxkBAAIc2WGd0R0_eTb0urBADTIOr4TWrFzQAAIZvDEbq6vwSJBp2UNlLEwQAQADAgADcwADIgQ',
    'tariffs_KZ_KZ_event': 'AgACAgIAAxkBAAIc22Gd0Slxnhq3PsbOC1MQX2bPvPfvAAIavDEbq6vwSKkwp-I4aef5AQADAgADcwADIgQ',
    'tariff_premium_RU': 'AgACAgIAAxkBAAIcZmGcjwEsKCWAad8Q5Bo-ymHYJTXAAAJXtjEbNQTgSGpWezgsGceHAQADAgADcwADIgQ',
    'tariff_premium_KZ': 'AgACAgIAAxkBAAIcaGGcjwsg1Ila5OHb3xXiV9cAAQ3cvAACWLYxGzUE4EjFpodAAAGQ6_gBAAMCAANzAAMiBA',
    'tariff_premium_max_RU': 'AgACAgIAAxkBAAIcamGcjxPPG7qXJUOZIAXyI_LFUrJdAAJZtjEbNQTgSHWJh8wguRHsAQADAgADcwADIgQ',
    'tariff_premium_max_KZ': 'AgACAgIAAxkBAAIcbGGcjxn6uVYWyVFx7vNHngZbkjqPAAJatjEbNQTgSGPiG7Kp6OgaAQADAgADcwADIgQ',
    'cosmo_girl': 'AgACAgIAAxkBAAIb3WGbW17DPiebizVxnMuIujqpinmfAAJhtjEbwBjYSKBMjaJIah99AQADAgADcwADIgQ',
}

ADMIN_MENU_TEXT = """
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
+5 вопросов админу:
/up_admin_daily_limit
+3 дня использования всем!
/up_time_limit_for_all_at_days_03
+30 дней использования всем!
/up_time_limit_for_all_at_days_30
50% скидка лузерам
/set_50_percent_price_for_losers
Удалить Автошколу из базы:
/delete_auto_school
Установить команды:
/set_commands

Узнать о пользователе:
/get_user_info
Показать статистику:
/statistics
"""
