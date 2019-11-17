# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ConferenceItem(scrapy.Item):
    name = scrapy.Field()
    abbr = scrapy.Field()
    description = scrapy.Field()
    s_date = scrapy.Field()
    e_date = scrapy.Field()
    paper_date = scrapy.Field()
    noti_date = scrapy.Field()
    year = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    organization = scrapy.Field()
    rank_CCF = scrapy.Field()
    rank_CORE = scrapy.Field()
    rank_QUALIS = scrapy.Field()
    indexes = scrapy.Field()
    need_confirm = scrapy.Field()