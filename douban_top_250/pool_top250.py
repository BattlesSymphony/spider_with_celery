import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from multiprocessing import Pool
import multiprocessing

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
	

def main():
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	for url in urls:
		parse_html(url)
if __name__ == '__main__':
	t1 = time.time()
	MAX_WORKER_NUM = multiprocessing.cpu_count()
	pool = Pool(MAX_WORKER_NUM)
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	for url in urls:
		pool.apply_async(parse_html, args=(url, ))	
	pool.close()
	pool.join()	

	print(time.time() - t1)
	# 2.167656898498535