# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value


def process_price(value):
    try:
        new_value = float(value)
    except:
        # print('Price Error', value)
        new_value = None
    return new_value


class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    ph_path = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    description = scrapy.Field()
