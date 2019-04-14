import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio


async def fetch(session, url, headers):
	async with session.get(url, headers=headers) as response:
		return await response.text()

async def job(url, headers):
	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url, headers)
		soup = BeautifulSoup(html, 'lxml')
		items = soup.select('ol.grid_view li')
		for item in items:
			title = item.select('span.title')[0].get_text()
			score = item.select('span.rating_num')[0].get_text()
			print(title, score)

	

def main():
	headers = {
		'User-Agent': UserAgent().random
	}
	t1 = time.time()
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	loop = asyncio.get_event_loop()
	tasks = [job(url, headers) for url in urls]
	# equal 
	'''
	tasks = []
	for url in urls:
		tasks.append(url)
	'''

	# 下面两种方式都可以
	# loop.run_until_complete(asyncio.wait(tasks))
	loop.run_until_complete(asyncio.gather(*tasks))
	print("耗时：", time.time()-t1)
	# 2.1750435829162598


if __name__ == '__main__':
	main()