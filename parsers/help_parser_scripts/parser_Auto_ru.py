# goroscop_list = ['capricorn', 'aries', 'taurus', 'gemini', 'cancer', 'leo',
# 'virgo', 'libra', 'scorpio', 'sagittarius', 'aquarius', 'pisces']

# from_date_list = ['yesterday', 'today', 'tomorrow', 'week', 'month', 'year']

# url = f"https://horo.mail.ru/prediction/{goroscop_list[0]}/{from_date_list[5]}/"
# html_text = requests.get(url).text

# tree = lxml.html.document_fromstring(html_text)
# title = tree.xpath('/html/body/div[3]/div[4]/div[2]/div[4]/div/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/span/h1/text()')
# body_text = tree.xpath('/html/body/div[3]/div[4]/div[2]/div[4]/div/div/div/div[2]/div/div/div[2]/div[4]/div/div//text()')
# print(title[0])
# for el in body_text:
# 	print(el.strip())

import requests
import lxml.html
from requests import get
from bs4 import BeautifulSoup


def decoder(text):
	text = text.replace('Â\xa0', '')
	text = text.replace('Â\xad', '')
	text = text.replace('\xa0', ' ')
	text = text.replace('\xad', ' ')
	text = text.encode('latin-1').decode('utf-8')
	text = text.replace('\n', ' ')
	text = text.strip()
	return text


all_questions = []


for page_number in range(1,51):
	try:
		url = f"https://mag.auto.ru/article/trafficregulations{page_number}/"
		html_text = requests.get(url).text
		tree = lxml.html.document_fromstring(html_text)

		question_id = page_number

		title = tree.xpath('/html/body/div[3]/div/article/section[4]/div/div/h2/text()')[0]
		title = decoder(title)

		answer1 = tree.xpath('/html/body/div[3]/div/article/section[4]/div/div/div[1]/label/div/text()')[0]
		answer1 = decoder(answer1)

		answer2 = tree.xpath('/html/body/div[3]/div/article/section[4]/div/div/div[2]/label/div/text()')[0]
		answer2 = decoder(answer2)

		soup = BeautifulSoup(get(url).text, 'html.parser')
		res = soup.find('input', {"class":"jrnl-radio", 'data-correct':"1"})
		correct_answer_id = res['id']
		answers = soup.find('label', {"for" : correct_answer_id}).find('div', {"class" : "jrnl-answer-text"})
		correct_answer = decoder(answers.text)

		explanations = soup.findAll('div', {"class":"jrnl-question-comment"})
		explanation1 = decoder(explanations[0].text).replace('Правильно!', '').strip()
		explanation2 = decoder(explanations[1].text).replace('Непрaвильно!', '').strip()


		text = {'id': question_id, 'question': title, 'all_answers': [answer1, answer2], 'correct_answer': correct_answer,
		'image_code': '', 'explanation': explanation2}

		all_questions.append(text)
	except IndexError:
		pass

for question in all_questions:
	print(question, end=',\n')

# url = f"https://mag.auto.ru/article/trafficregulations27/"
# soup = BeautifulSoup(get(url).text, 'html.parser')

# explanations = soup.findAll('div', {"class":"jrnl-question-comment"})
# explanation2 = explanations[1].text.strip()
# print(explanation2)