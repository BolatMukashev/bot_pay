from requests import get
from bs4 import BeautifulSoup
from pprint import pprint

url = f"https://auto.mail.ru/info/penalty/#skorostnoi_rezhim"
soup = BeautifulSoup(get(url).text, 'html.parser')

titles = soup.find_all('td', {"class": "p-penalties__cell"})
all_titles = [el.find('span') for el in titles]
all_titles = [{x.text: []} for x in all_titles if x]

pprint(all_titles, depth=3, width=300)

print()

all_values = soup.find_all('tr', {"class": "p-penalties__row"})
values1 = []
for el in all_values:
    result = el.find_all('td', {"class": "p-penalties__cell"})
    try:
        res = {'simple_title': '',
               'title': result[1].text.replace('\n', ''),
               'penalty': result[2].text.replace('\xa0', ' ')}
        values1.append(res)
    except IndexError:
        pass

pprint(values1, depth=3, width=1000)
