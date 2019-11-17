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
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if(spider.name == 'conference_hb'):
            sql = '''insert into t_conference_hb(name,abbr,description,s_date,e_date,paper_date,noti_date,year,address,website,organization,rank_CCF,rank_CORE,rank_QUALIS,indexes,need_confirm) 
                    value( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        elif(spider.name == 'conference_all'):
            sql = '''insert into t_conference_all(name,abbr,description,s_date,e_date,paper_date,noti_date,year,address,website,organization,rank_CCF,rank_CORE,rank_QUALIS,indexes,need_confirm) 
                    value( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

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
            item.get('indexes', ''),
            item.get('need_confirm', 0)
        )
        try:
            self.cursor.execute(sql, value)
            self.conn.commit()
            spider.successDB()
        except Exception as e:
            print("【DB ERROR】", str(e))
            self.conn.rollback()
            spider.errorIndex(item.get('abbr', 'unknow'))
        return item

    # 关闭数据库
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        spider.savaIndex()