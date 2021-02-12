from db_operation import create_new_json_file

auto_schools = [
    {'school_name': 'Болат', 'country': 'Казахстан', 'city': 'Уральск', 'phones': [87775552233, 85552223311],
     'emails': ['m-bolat@mail.ru']},
    {'school_name': 'Кими', 'country': 'Казахстан', 'city': 'Орал', 'phones': [81452223321],
     'emails': ['ya.ne.angel.kimi@gmail.com']},
]
# {'school_name': '', 'country': 'Казахстан', 'city': 'Уральск', 'phones': [], 'emails': []},


create_new_json_file('auto_schools.json', auto_schools)
