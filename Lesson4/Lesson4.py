'''
1)Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
Для парсинга использовать xpath. Структура данных должна содержать:
название источника, наименование новости, ссылку на новость, дата публикации
2)Сложить все новости в БД
'''

from pprint import pprint
from lxml import html
import requests
from datetime import date, timedelta
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['news_db']
news_get = db.news_db

news_get.delete_many({})


def db_news_update(data):
    news_get.update(data, {'upsert': True})


def request_to_lenta():
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': '*/*'}
    lenta_link = 'https://lenta.ru'
    response = requests.get(lenta_link, headers=header)
    dom = html.fromstring(response.text)

    news_data = []
    items = dom.xpath("//a[@href]")
    l = 0
    for item in items:
        if len(item.xpath('./time')) != 0:
            name = str(item.xpath('./text()')[0])
            name = name.replace('\xa0', ' ')
            time = str(item.xpath('./time/@datetime')[0])
            news = {}
            #
            link = item.xpath("./@href")

            news['name'] = name
            if str(link[0]).find('http') == -1:
                news['link'] = lenta_link + str(link[0])
            else:
                news['link'] = str(link[0])

            news['source'] = lenta_link
            news['time'] = time
            news['web-site'] = lenta_link
            # news['news_data'] = data
            news_data.append(news)
            # db_news_update(news)
            l += 1
    print(f'Обработано {l} новостей с {lenta_link}')
    news_get.insert_many(news_data)
    return (news_data)


def request_to_yandex():
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': '*/*'}
    yandex_link = 'https://yandex.ru/news'
    response = requests.get(yandex_link, headers=header)
    dom = html.fromstring(response.text)

    news_data = []
    items = dom.xpath("//h2[@class='story__title']/a/../../parent::*")
    l = 0
    for item in items:
        news = {}
        data = item.xpath(".//text()")
        link = item.xpath(".//@href")

        dtime = str(date.today())
        ydtime = str(date.today() - timedelta(days=1))
        if len(data) == 1:
            name = data[0]
            source = data[1][:-6]
            time = data[1][-5:]
        else:
            time = data[len(data) - 3][-5:]
            source = data[len(data) - 3][:-6]
            name = ''
            for i in range(len(data) - 3):
                name = name + str(data[i])

        if source.find("вчера") != -1:
            source = source[:-11]
            time = ydtime + ' ' + time
        else:
            time = dtime + ' ' + time

        news['name'] = name
        news['link'] = yandex_link + str(link[0])
        news['source'] = source
        news['time'] = time
        news['web-site'] = yandex_link
        # news['news_data'] = data
        l += 1
        news_data.append(news)
        # db_news_update(news)
    print(f'Обработано {l} новостей с {yandex_link}')
    news_get.insert_many(news_data)
    return (news_data)


def request_to_mail():
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': '*/*'}
    mailru_link = 'https://news.mail.ru/'
    response = requests.get(mailru_link, headers=header)
    dom = html.fromstring(response.text)

    news_data = []
    items = dom.xpath("//div[@class='newsitem newsitem_height_fixed js-ago-wrapper']")
    l = 0
    for item in items:
        data = item.xpath("./..//text()")
        link = item.xpath(".//@href")
        time = str(item.xpath('.//@datetime')[0])
        source = data[2]
        for d in range(3, len(data)):
            news = {}
            if d != 4:
                news['name'] = str(data[d]).replace('\xa0', ' ')
                news['link'] = mailru_link + str(link[0])
                news['source'] = source
                news['time'] = time
                news['web-site'] = mailru_link
                # news['news_data'] = data
                # pprint(news)
                news_data.append(news)
                # db_news_update(news)
                l += 1
    print(f'Обработано {l} новостей с {mailru_link}')
    news_get.insert_many(news_data)
    return (news_data)


request_to_lenta()
request_to_yandex()
request_to_mail()
