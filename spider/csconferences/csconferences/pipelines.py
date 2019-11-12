# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from csconferences import settings


class ConferencePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            db = settings.MYSQL_DBNAME,
            charset = 'utf8',
            user_unicode = True
        )
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        return item
