import json
from db_operations import *
from auto_schools import auto_schools
from pprint import pprint
from db_operations import new_pay_order
from peewee import IntegrityError

# проверяем длину вопроса - 255, ответов - 100, пояснений - 200

db_list = []


def test_questions_in_db(db_name):
    print('questions:', end=' ')
    question_limit_out_list = []
    for idd, el in enumerate(db_name):
        if len(el['question']) > 255:
            question_limit_out_list.append(f'line {idd + 1} -> len {len(el["question"])}')

    if len(question_limit_out_list) > 0:
        print(f'{len(question_limit_out_list)} excess')
        for el in question_limit_out_list:
            print(el)
    else:
        print('all good')


def test_answers_in_db(db_name):
    print('answers:', end=' ')
    answer_limit_out_list = []
    for idd, el in enumerate(db_name):
        for column, answer in enumerate(el['all_answers']):
            if len(answer) > 100:
                answer_limit_out_list.append(f'line {idd + 1} -> id {column} -> len {len(answer)}')

    if len(answer_limit_out_list) > 0:
        print(f'{len(answer_limit_out_list)} excess')
        for el in answer_limit_out_list:
            print(el)
    else:
        print('all good')


def test_correct_answers_in_db(db_name):
    print('correct_answers:', end=' ')
    correct_answer_limit_out_list = []
    for idd, el in enumerate(db_name):
        if el['correct_answer'] not in el['all_answers']:
            correct_answer_limit_out_list.append(f'line {idd + 1}')

    if len(correct_answer_limit_out_list) > 0:
        print(f'{len(correct_answer_limit_out_list)} excess')
        for el in correct_answer_limit_out_list:
            print(el)
    else:
        print('all good')


def test_explanations_in_db(db_name):
    print('explanations:', end=' ')
    explanation_limit_out_list = []
    for idd, el in enumerate(db_name):
        if len(el['explanation']) > 200:
            explanation_limit_out_list.append(f'line {idd + 1} -> len {len(el["explanation"])}')

    if len(explanation_limit_out_list) > 0:
        print(f'{len(explanation_limit_out_list)} excess')
        for el in explanation_limit_out_list:
            print(el)
    else:
        print('all good')


def all_db_testing(questions_list):
    for idd, el in enumerate(questions_list):
        print(f'Data base {idd + 1} testing...........')
        test_questions_in_db(el)
        test_answers_in_db(el)
        test_correct_answers_in_db(el)
        test_explanations_in_db(el)
        print()


all_db_testing(db_list)


# pprint(data, depth=3, width=300)

class TestAutoSchool:
    school_name = 'TestCalss'
    country = 'Urugvai'
    city = 'Racon'
    phones = ['8777755', '556611122']
    emails = ['testclass@mail.ru']
    instagram = 'test_instagram'
    registration_date = '2021-02-13'
    secret_key = 'ttttttyyyyyyy'
    promo_code = 'simple_dimple'
    number_of_references = 5
    notified = False


def test_pay_order():
    telegram_id = 55447789
    order_number = 555555445
    price = 100
    try:
        new_pay_order(telegram_id, order_number, price)
    except Exception as err:
        print(err)


def test_auto_schools():
    school_name = 'TestSchool'
    country = 'Казахстан'
    city = 'Уральск'
    phones = ''
    emails = ''
    instagram = ''
    secret_key = 'test26'
    promo_code = 'testpr55omo'
    try:
        AutoSchool(school_name=school_name,
                   country=country,
                   city=city,
                   secret_key=secret_key,
                   promo_code=promo_code).save()
    except IntegrityError as err:
        print(err.args[1])


if __name__ == '__main__':
    a = get_all_auto_schools_on_db()
    b = get_not_notified_auto_schools_on_db()
    # edit_auto_school_by('YjQ4BC6CZcnd4wO0O32CDF', 'phones', [8777, 9777])
    schools = get_all_auto_schools_on_dict_format(a)
    edit_auto_school_by('grpm5U0Ia9Clcjv5HkQRMX', 'emails', ['dfdf-erf-dfdfd-vv@mail.kz', 'm-bolat@mail.ru'])
    for x in schools[-3:]:
        print(x)
        print()
