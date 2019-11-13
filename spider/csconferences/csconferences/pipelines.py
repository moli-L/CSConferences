# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from csconferences import settings


class ConferencePipeline(object):
    # 连接数据库
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DBNAME,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''insert into t_conference(name,abbr,description,s_date,e_date,paper_date,noti_date,year,address,website,organization,rank_CCF,rank_CORE,rank_QUALIS) 
                value( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        value = (
            item.get('name', ''),
            item.get('abbr', ''),
            item.get('description', ''),
            item.get('s_date', None),
            item.get('e_date', None),
            item.get('paper_date', None),
            item.get('noti_date', None),
            item.get('year', None),
            item.get('address', ''),
            item.get('website', ''),
            item.get('organization', ''),
            item.get('rank_CCF', ''),
            item.get('rank_CORE', ''),
            item.get('rank_QUALIS', ''),
        )
        try:
            self.cursor.execute(sql, value)
            self.conn.commit()
        except Exception as e:
            print("【DB ERROR】", str(e))
            self.conn.rollback()
            spider.errorIndex()
        return item

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        spider.savaIndex()
