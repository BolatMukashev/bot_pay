from db_operation import create_new_json_file

auto_schools = [
    {'school_name': 'Сапар', 'country': 'Казахстан', 'city': 'Уральск', 'phones': [87775552233, 85552223311],
     'emails': ['ggg@mail.ru']},
    {'school_name': 'Кими', 'country': 'Казахстан', 'city': '', 'phones': [81452223321],
     'emails': ['ggg@mail.ru', 'kkk@mail.ru']},
]
# {'school_name': '', 'country': 'Казахстан', 'city': 'Уральск', 'phones': [], 'emails': []},


create_new_json_file('auto_schools.json', auto_schools)
