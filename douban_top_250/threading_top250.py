import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import threading 
import time

ua = UserAgent()	
headers = {
	'User-Agent': ua.random
}

def get_html(url):
	try:
		r = requests.get(url, headers=headers)
		if r.status_code == 200:
			return r.content.decode('utf-8')
	except:
		return None

def parse_html(url):
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	items = soup.select('ol.grid_view li')
	for item in items:
		title = item.select('span.title')[0].get_text()
		score = item.select('span.rating_num')[0].get_text()
		print(title, score)
	print('======'*4)

if __name__ == '__main__':
	t1 = time.time()
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	threads = [threading.Thread(target=parse_html, args=(url, )) for url in urls]
	for thread in threads:
		thread.start()
		thread.join()
	print(time.time() - t1)