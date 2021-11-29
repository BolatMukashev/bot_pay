import re

file_name = 'test.txt'

with open(file_name, encoding='utf-8', mode='r', newline='') as f:
    stroka = f.read()

result = re.split(r'Статья \d{3}', stroka)
del (result[0])

vopros = []

for el in result:
    el = el.replace('\r', '')
    el = el.replace('\n', '')
    description = re.findall(r'Примечание\..+', el)
    try:
        description = description[0]
        el = re.sub(r'Примечание\..+', '', el)
    except IndexError:
        description = ''
    res = re.split(r'\d\. |\d-\d\. ', el)
    item = {'small_title': '', 'title': res[0], 'answers': res[1:], 'description': description}
    vopros.append(item)

for el in vopros:
    print(el, end=',\n')
