import json

from db_operation import get_image_codes_from, add_image_code_to, translate_db_to_kz_language, get_data_from_json_file, \
    beautiful_print_data_from_dict
from questions_ru1 import questions_ru1
from questions_ru2 import questions_ru2
from questions_ru3 import questions_ru3
from questions_kz1 import questions_kz1
from questions_kz2 import questions_kz2
from questions_kz3 import questions_kz3

# проверяем длину вопроса - 255, ответов - 100, пояснений - 200

db_list = [questions_ru1, questions_ru2, questions_ru3, questions_kz1, questions_kz2, questions_kz3]


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


def all_db_testing(db_list):
    for idd, el in enumerate(db_list):
        print(f'Data base {idd + 1} testing...........')
        test_questions_in_db(el)
        test_answers_in_db(el)
        test_correct_answers_in_db(el)
        test_explanations_in_db(el)
        print()


all_db_testing(db_list)

# translate_db_to_kz_language(questions_ru3, 'kz.json')
# data = get_data_from_json_file('kz.json')
# beautiful_print_data_from_dict(data)
