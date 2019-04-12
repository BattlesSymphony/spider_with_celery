import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from multiprocessing import Pool, Queue
import multiprocessing

class Douban(object):
	def __init__(self):
		self.ua = UserAgent()	
		self.headers = {
			'User-Agent': self.ua.random
		}
		self.MAX_WORKER_NUM = multiprocessing.cpu_count()
		self.urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
		self.queue_list = Queue()

	def get_html(self, url):
		try:
			r = requests.get(url, headers=self.headers)
			if r.status_code == 200:
				return r.content.decode('utf-8')
		except:
			return None

	def parse_html(self, url):
		print('hi am in')
		html = self.get_html(url)
		soup = BeautifulSoup(html, 'lxml')
		items = soup.select('ol.grid_view li')
		for item in items:
			title = item.select('span.title')[0].get_text()
			score = item.select('span.rating_num')[0].get_text()
			print(title, score)

	# 类中学多进程。。 实现不了。。。
	def multiprocess_get(self):
		print(self.MAX_WORKER_NUM)
		pool = Pool(self.MAX_WORKER_NUM)
		for url in self.urls:
			self.queue_list.put(url)
		while self.queue_list.qsize() > 0:
			pool.apply_async(self.parse_html, args=(self.queue_list.get(), ))
		pool.close()
		pool.join()

	def main(self):
		t1 = time.time()
		self.multiprocess_get()
		print(time.time() - t1)


if __name__ == '__main__':
	d = Douban()
	d.main()
