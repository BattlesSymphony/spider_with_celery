import time
from random import randint
import wechatsogou
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from top250.models import Movie
from top250.celery import app

ua = UserAgent()	
headers = {
	'User-Agent': ua.random
}

@app.task
def main():
	urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
	for url in urls:
        # save_topic.apply_async(args=[topic_data])
		parse_html.apply_async(args=[url])


@app.task       
def parse_html(url):
    html = requests.get(url, headers=headers).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('ol.grid_view li')
    for item in items:
        movie_data = {}
        name = item.select('span.title')[0].get_text()
        score = item.select('span.rating_num')[0].get_text()
        try:
            Movie.objects.get(name=name)
            continue
        except Movie.DoesNotExist:
            movie_data['name'] = name
            movie_data['score'] = score
            try:
                save_movie.apply_async(args=[movie_data])
            except Exception as e:
                print(e)

@app.task
def save_movie(movie_data):
    movie = Movie(**movie_data)
    movie.save()


# @app.task
# def get_topic(wechat_id):
#     topics_list = ws_api.get_gzh_article_by_history(wechat_id)
#     topics_list = topics_list.get('article')
#     for i in topics_list:
#         topic_data = {}
#         uniqueid = get_uniqueid('%s:%s' % (wechat_id, i["title"]))
#         try:
#             Topic.objects.get(uniqueid=uniqueid)
#             continue
#         except Topic.DoesNotExist:
#             topic_data['uniqueid'] = uniqueid
#             topic_data["wechat_id"] = wechat_id
#             topic_data["abstract"] = i["abstract"]
#             topic_data["title"] = i["title"]
#             topic_data["avatar"] = i["cover"]
#             topic_data["url"] = i["content_url"] + \
#                 "&devicetype=Windows-QQBrowser&version=61030004&pass_ticket=qMx7ntinAtmqhVn+C23mCuwc9ZRyUp20kIusGgbFLi0=&uin=MTc1MDA1NjU1&ascene=1"
#             topic_data["publish_time"] = i["datetime"]
#             try:
#                 source = ws_api.get_article_content(topic_data["url"])[
#                     "content_html"]
#                 topic_data["source"] = source
#                 # process_topic(topic_data)
#                 save_topic.apply_async(args=[topic_data])
#                 time.sleep(randint(1, 5))
#             except Exception as e:
#                 print(e)

# @app.task
# def save_topic(topic_data):
#     topic = Topic(**topic_data)
#     topic.save()
