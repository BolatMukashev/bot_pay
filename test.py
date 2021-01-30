import json

from questions_ru1 import bad_db
from questions_ru2 import bad_db2
from questions_kz1 import bad_db_kz1
from questions_kz2 import bad_db_kz2

# проверяем длину вопроса - 255, ответов - 100, пояснений - 200

db_to_test = bad_db_kz2


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


test_questions_in_db(db_to_test)
test_answers_in_db(db_to_test)
test_correct_answers_in_db(db_to_test)
test_explanations_in_db(db_to_test)