from questions_ru1 import bad_db
from questions_ru2 import bad_db2
from questions_kz1 import bad_db_kz1

# проверяем длину вопроса - 255, ответов - 100, пояснений - 200

db_to_testing = bad_db_kz1

print('questions:', end=' ')
question_limit_out_list = []
for idd, el in enumerate(db_to_testing):
    if len(el['question']) > 255:
        question_limit_out_list.append(f'line {idd + 1} -> len {len(el["question"])}')

if len(question_limit_out_list) > 0:
    print(f'{len(question_limit_out_list)} excess')
    for el in question_limit_out_list:
        print(el)
else:
    print('all good')


print('answers:', end=' ')
answer_limit_out_list = []
for idd, el in enumerate(db_to_testing):
    for column, answer in enumerate(el['all_answers']):
        if len(answer) > 100:
            answer_limit_out_list.append(f'line {idd + 1} -> id {column} -> len {len(answer)}')

if len(answer_limit_out_list) > 0:
    print(f'{len(answer_limit_out_list)} excess')
    for el in answer_limit_out_list:
        print(el)
else:
    print('all good')


print('correct_answers:', end=' ')
correct_answer_limit_out_list = []
for idd, el in enumerate(db_to_testing):
    if el['correct_answer'] not in el['all_answers']:
        correct_answer_limit_out_list.append(f'line {idd + 1}')

if len(correct_answer_limit_out_list) > 0:
    print(f'{len(correct_answer_limit_out_list)} excess')
    for el in correct_answer_limit_out_list:
        print(el)
else:
    print('all good')


print('explanations:', end=' ')
explanation_limit_out_list = []
for idd, el in enumerate(db_to_testing):
    if len(el['explanation']) > 200:
        explanation_limit_out_list.append(f'line {idd + 1} -> len {len(el["explanation"])}')

if len(explanation_limit_out_list) > 0:
    print(f'{len(explanation_limit_out_list)} excess')
    for el in explanation_limit_out_list:
        print(el)
else:
    print('all good')


import json
# показать красиво:
# print(json.dumps(bad_db2, sort_keys=True, indent=4, ensure_ascii=False))

# # записать в json
# with open('test.json', 'w', encoding='utf-8') as json_file:
#     json.dump(bad_db2, json_file, ensure_ascii=False)
#
# # прочесть json
# with open('test.json', 'r', encoding='utf-8') as json_file:
#     data = json.load(json_file)
