import scrapy
from scrapy.http import HtmlResponse
from leroyparser.leroy.items import LeroyItem
from scrapy.loader import ItemLoader

class LeroyruSpider(scrapy.Spider):
    name = 'leroyru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, catalogue):
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{catalogue}/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a[@href]").extract_first()
        links = response.css('a.black-link.product-name-inner::attr(href)').extract()

        for link in links:
            yield response.follow(link, callback=self.links_parse)
        yield response.follow(next_page, callback=self.parse)

    def links_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('ph_path', "//uc-pdp-card-ga-enriched[@class='card-data']/uc-pdp-media-carousel/img/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('price',"//uc-pdp-price-view[@class='primary-price']/span/text()")
        loader.add_xpath('description', "//section[@id='nav-characteristics']//text()")
        loader.add_xpath('photos', "//uc-pdp-card-ga-enriched[@class='card-data']/uc-pdp-media-carousel/img/@src")
        yield loader.load_item()

