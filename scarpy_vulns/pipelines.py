# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging
from . import settings

class ScarpyVulnsPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,  # 数据库地址
            port=settings.MYSQL_PORT,  # 数据库端口
            db=settings.MYSQL_DB,  # 数据库名
            user=settings.MYSQL_USER,  # 数据库用户名
            passwd=settings.MYSQL_PASSWD,  # 数据库密码
            charset=settings.MYSQL_CHARSET,  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        # count插入重复计数,flag标记做辅助关闭所有线程
        self.count = 0
        self.flag = 0

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT INTO list(time, title, rank, author ,organization, type)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (item['time'], item['title'], item['rank'], item['author'], item['organization'], item['type'])
                ) # item里面定义的字段和表字段对应
            # 提交sql语句
            self.connect.commit()
            self.count = 0

        except Exception as e:
            self.connect.rollback()
            # 1062 Duplicate entry 重复实体错误
            if e.__str__()[1:5] == '1062':
                self.count += 1
                if self.count >= 10:    # 连续重复10次
                    if self.flag == 1:
                        spider.crawler.engine.close_spider(spider, u'[*]爬虫停止。。。')
                    else:
                        if input(u"[-]数据库插入异常，可能已经爬取到重复数据，是否继续爬取？Y/n :") == 'n':
                            spider.crawler.engine.close_spider(spider, u'[*]爬虫停止。。。')
                            self.flag = 1
                        else:
                            print(u"[*]爬虫继续。。。")
                            self.count = 0
                else:
                    pass
            else:
                print(e)

        return item

    # 爬虫停止时关闭数据库连接
    def close_spider(self, spider):
        spider.crawler.engine.close_spider(spider, u'[*]爬虫停止。。。')
        self.connect.close()