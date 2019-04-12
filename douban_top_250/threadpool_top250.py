import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import  Queue
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

if __name__ == '__main__':
	t1 = time.time()
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	pool = ThreadPoolExecutor()
	queue_list = Queue()
	for url in urls:
		queue_list.put(url)
	while queue_list.qsize() > 0:
		pool.submit(parse_html, queue_list.get())
	# 1.8085618019104004
	# pool = ProcessPoolExecutor()
	# 2.313598871231079
	
	# for url in urls:
	# 	pool.submit(parse_html, url)
	pool.shutdown(wait=True)
	print(time.time() - t1)
