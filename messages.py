MESSAGE = dict(start_admin_text="""
Показать статистику:
/statistics

MESSAGES
Отправить картинку + подпись:
/send_post
Cообщение для неоплативших:
/send_message_from_losers

EMAIL
Отправить приветственное сообщениe:
/send_hello_emails_to_new_schools
Отправить email всем Автошколам:
/send_email_for_all_auto_schools

ACTIONS
+3 минуты админу:
/up_admin_time_limit
+3 дня использования всем!
/up_time_limit_for_all_at_3day
+30 дней использования всем!
/up_time_limit_for_all_at_30days
Удалить Автошколу из базы:
/delete_auto_school
Бэкап данных:
/backup_all_data
Установить команды:
/set_commands
""",
               start_user_text='Добро пожаловать\n'
                               'У вас есть 24 часа чтобы ознакомится с нашей Образовательной платформой',
               language_choice='Выберите язык\n'
                               '------------------------\n'
                               'Тілді таңдаңыз',
               language_set_ok_RU='Язык изменён ✓',
               language_set_ok_KZ='Тіл өзгерді ✓',
               country_choice_RU='Из какой Вы страны?',
               country_choice_KZ='Сіз қай елденсіз?',
               country_edited_ok_RU='Страна выбрана ✓',
               country_edited_ok_KZ='Ел таңдалды ✓',
               registration_ok_RU='Регистрация прошла успешно!\nНажми кнопку СТАРТ',
               registration_ok_KZ='Тіркеу сәтті аяқталды!\nСТАРТ батырмасын басыңыз',
               info_RU='Telegram налагает ограничения на количество символов в тексте при составлении опросов '
                       'и викторин.\n'
                       'Поэтому некоторые слова в ответах были заменены на более короткие аналоги, например:\n'
                       'транспорное средство -> транспорт -> авто -> ТС\n'
                       'А конструкции вида дом/дорога/машина - означают:\n'
                       'дом или дорога или машина',
               info_KZ='Telegram сауалнамалар мен викториналар құрғанда мәтіндегі таңбалар санына шектеулер қояды.\n'
                       'Сондықтан жауаптардағы кейбір сөздер қысқа аналогтармен ауыстырылды.'
                       'Мысалы, көлік құралы -> көлік',
               limit_error_RU="Просим прощения, но Ваш пробный период закончился.\n\n"
                              "Произведите оплату, чтобы и дальше пользоваться нашим замечательным сервисом.\n\n"
                              "Чтобы произвести оплату нажмите 👉🏻 /pay\n\n"
                              "Для активации ПРОМОКОДА нажмите 👉🏻 /promo_code\n\n"
                              "❗️ВНИМАНИЕ❗️\n"
                              "Чтобы продолжить обучение после оплаты нажмите 👉🏻 /question",
               limit_error_KZ='Кешіріңіз, бірақ сіздің сынақ мерзіміңіз аяқталды.\n\n'
                              'Біздің тамаша қызметімізді пайдалануды жалғастыру үшін төлем жасаңыз.\n\n'
                              'Төлем жасау үшін /pay басыңыз\n\n'
                              'ПРОМКОД қосу үшін /promo_code басыңыз\n\n'
                              'НАЗАР АУДАРЫҢЫЗ\n'
                              'Төлемнен кейін оқытуды жалғастыру үшін /question басыңыз',
               pay_message_RU='Получите ГОД безлемитного доступа к нашей образовательной платформе.\n'
                              'Для Вас это будет стоить всего',
               pay_message_KZ='Біздің білім беру платформасына БIР ЖЫЛ шектеусіз қол жеткізіңіз.\n'
                              'Сіз үшін бұл бар болғаны',
               pay_registered_message_RU='Поздравляем! Ваш платёж принят.',
               pay_registered_message_KZ='Құттықтаймыз! Сіздің төлеміңіз қабылданды.', bot_link_RU='Вернуться к боту',
               bot_link_KZ='Ботқа оралу',
               link_to_chat_RU='Обсудить вопросы 👉🏻 https://t.me/pdd_forum',
               link_to_chat_KZ='Сұрақтарды талқылау 👉🏻 https://t.me/pdd_forum',
               link_error_chat_RU='Сообщить об ошибке 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy',
               link_error_chat_KZ='Қате туралы хабарлау 👉🏻 https://t.me/joinchat/g5wLf231F-RlNTYy')

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
    '100friends_RU': 'Акция! Приведи друга и получи +1 день бесплатного пользования нашей образовательной платформой!',
    '100friends_KZ': 'Қор! Досыңды әкел және біздің білім беру платформасын +1 күн ақысыз пайдаланыңыз!',
    '100friends_action_message1_RU': '⬇️ Вот твоя ссылка! Отправляй её друзьям ⬇️',
    '100friends_action_message2_RU': 'Бот, который поможет:\n'
                                     '🔹 Подготовится к экзамену на знание ПДД\n'
                                     '🔹 Закрепить полученные в автошколе знания',
    '100friends_action_message1_KZ': '⬇️ Міне сілтеме! Достарыңызға жіберіңіз ⬇️',
    '100friends_action_message2_KZ': 'Бот көмектеседі:\n'
                                     '🔹 Жол қозғалысы ережелерін білу бойынша емтиханға дайындалуға\n'
                                     '🔹 Автомектепте алған білімдерін бекіту'
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

STICKERS = {
    'hello': 'CAACAgIAAxkBAAEB1rxgGo2hRDlaGoiEHOZf3mY6C19jKQACKwIAArnzlwv7BQOMjG9ozB4E',
    'repair': 'CAACAgIAAxkBAAEB1rhgGo2MKy7iUaRUUGj5b1LO4V0sHgACMQEAArnzlws-7wljOEZF0x4E',
    'message': 'CAACAgIAAxkBAAEB1rpgGo2RcuS-bNqr3URmqOIh9Nv3SAACPAEAArnzlwvMnvUK9IcNFR4E',
    'come_back': 'CAACAgIAAxkBAAEB1sRgGpJtzbzRtNodSiGctvngZ9AccQACHwEAArnzlwu5r6hVbS11sB4E',
    'all_good': 'CAACAgIAAxkBAAEB1sJgGpJkbNi5ocJafzCeo8OUd7b_VQACJgEAArnzlwt4WnW4BxSuMB4E',
    'NO': 'CAACAgIAAxkBAAEB3HtgIV_xw819XJj4oKtFyPqCyh_pxwACawEAArnzlwslqyJF_izS0h4E'
}

IMAGES = {
    '100friends': 'AgACAgIAAxkBAAI9mmDhhtWeuMCQ_jCRRgABOuH3RU2X_gACZ7QxGxJDEEv-BXPviTTuPwEAAwIAA3MAAyAE'
}

PROMO_CODE = {
    'registered': 'Данный промокод уже зарегистрирован',
    'error': 'Промокод введен не верно',
    'promo_code_error_RU': 'Промокод не найден',
    'promo_code_error_KZ': 'Промокод табылмады',
    'promo_code_none_text_RU': 'Не использовался',
    'promo_code_none_text_KZ': 'Қолданылмаған',
    'promo_code_command_text_RU': 'Активируй промокод и получи 3 дня безлимитного доступа к нашей образовательной '
                                  'платформе.\n'
                                  'А ещё ты получишь 50% скидку на покупку годового доступа!',
    'promo_code_command_text_KZ': 'Промокод жазып, біздің білім беру платформасына 3 күндік шектеусіз қол жеткізіңіз.\n'
                                  'Сіз сондай-ақ жылдық қол жетімділікті сатып алғанда 50% жеңілдікке ие боласыз!',
    'promo_code_was_used_RU': 'Промокод уже был использован Вами ранее',
    'promo_code_was_used_KZ': 'Промокодты сіз бұрын қолданғансыз',
    'promo_code_activated_RU': 'Поздравляю! Промокод активирован 🎉',
    'promo_code_activated_KZ': 'Құттықтаймыз! Промокод белсендірілді 🎉'
}
