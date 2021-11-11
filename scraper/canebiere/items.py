# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CanebiereItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    nb_commentaires = scrapy.Field()
    full_text = scrapy.Field()
    html = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
