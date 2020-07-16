from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparser.leroy.spiders import leroyru
from leroyparser.leroy import settings

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(leroyru.LeroyruSpider, catalogue='cvetushchie-rasteniya')

    process.start()