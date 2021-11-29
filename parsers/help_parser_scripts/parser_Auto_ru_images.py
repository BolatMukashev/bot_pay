import os
import urllib.request
from bs4 import BeautifulSoup
from requests import get

this_path = os.getcwd()

for page_number in range(1,51):
	try:
		url = f"https://mag.auto.ru/article/trafficregulations{page_number}/"
		soup = BeautifulSoup(get(url).text, 'html.parser')
		img = soup.find("div", {"class":"jrnl-img"}).find("img")
		image_url = img['src']
		save_name = f'{page_number}.jpg'
		path = os.path.join(this_path, 'images', save_name)
		urllib.request.urlretrieve(image_url, path)
	except AttributeError:
		pass