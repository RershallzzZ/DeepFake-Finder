# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    promulgator = scrapy.Field()
    introduction = scrapy.Field()
    sha256 = scrapy.Field()
    category = scrapy.Field()
    duration = scrapy.Field()
    upload_time = scrapy.Field()
    crawl_time = scrapy.Field()
    video_path = scrapy.Field()
    screenshot_path = scrapy.Field()
    download = scrapy.Field()
    analyzed = scrapy.Field()
    conclusion = scrapy.Field()
    watchtime = scrapy.Field()