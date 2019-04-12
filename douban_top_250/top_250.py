import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

class Douban(object):
	def __init__(self):
		self.ua = UserAgent()	
		self.headers = {
			'User-Agent': self.ua.random
		}

	def get_html(self, url):
		try:
			r = requests.get(url, headers=self.headers)
			if r.status_code == 200:
				return r.content.decode('utf-8')
		except:
			return None

	def parse_html(self, url):
		html = self.get_html(url)
		soup = BeautifulSoup(html, 'lxml')
		items = soup.select('ol.grid_view li')
		for item in items:
			title = item.select('span.title')[0].get_text()
			score = item.select('span.rating_num')[0].get_text()
			print(title, type(title), score, type(score))

if __name__ == '__main__':
	t1 = time.time()
	d = Douban()
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	for url in urls:
		d.parse_html(url)
		print('======'*4)
	print(time.time() - t1)