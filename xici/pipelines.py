# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql

def dbHandle():
    conn = pymysql.connect(
        host='192.168.31.205',
        user='felix',
        passwd='abc123',
        charset='utf8',
        #use_unicode=False
    )
    return conn

class XiciPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into scrapy.news(title,url,content,inputtime) values (%s,%s,%s,%s)'
        #print(sql)

        inputtime = int(time.time())


        try:
            cursor.execute(sql,(dbObject.escape(item['title']),item['url'],dbObject.escape(item['content']),inputtime))
            dbObject.commit()
        except Exception as e:
            #print e
            dbObject.rollback()

        return item