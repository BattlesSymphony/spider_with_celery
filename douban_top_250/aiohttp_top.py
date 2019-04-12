import time
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio


async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def job(url):
	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url)
		soup = BeautifulSoup(html, 'lxml')
		items = soup.select('ol.grid_view li')
		for item in items:
			title = item.select('span.title')[0].get_text()
			score = item.select('span.rating_num')[0].get_text()
			print(title, score)

	

def main():
	t1 = time.time()
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	loop = asyncio.get_event_loop()
	tasks = [job(url) for url in urls]
	loop.run_until_complete(asyncio.wait(tasks))
	print("耗时：", time.time()-t1)
	# 2.1750435829162598
if __name__ == '__main__':
	main()