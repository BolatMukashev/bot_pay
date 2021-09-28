from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm as loading_bar

url_uralsk = 'https://2gis.kz/uralsk/search/%D0%90%D0%B2%D1%82%D0%BE%D1%88%D0%BA%D0%BE%D0%BB%D1%8B'
url_almaty = 'https://2gis.kz/almaty/search/%D0%90%D0%B2%D1%82%D0%BE%D1%88%D0%BA%D0%BE%D0%BB%D1%8B'
url_moscow = 'https://2gis.ru/moscow/search/%D0%90%D0%B2%D1%82%D0%BE%D1%88%D0%BA%D0%BE%D0%BB%D1%8B'

url_to_link = 'https://2gis.kz'
headers = {'User-Agent': 'Mozilla/5.0'}

urls = []

for i, x in enumerate(range(1, 11), start=1):
    req = Request(url_moscow + '/page/' + str(x), headers=headers)
    page = urlopen(req)
    print(i, page.geturl())

# for x in range(1, 11):
#     req = Request(url_almaty + '/page/' + str(x), headers=headers)
#     page = urlopen(req)
#     if page.getcode() == 200:
#         soup = BeautifulSoup(page, features="lxml")
#         cards = soup.find_all('div', class_="_y3rccd")
#         for i in loading_bar(cards, desc=f'page {x}'):
#             try:
#                 block = i.find('div', class_='_1h3cgic')
#                 school_url = block.find('a', href=True)
#                 school_name = school_url.find('span')
#                 urls.append(f'{school_name.text} {url_to_link + school_url.get("href")} ')
#             except Exception as ex:
#                 print(ex)
#
# print(urls)
