# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import ScarpyVulnsItem

class SrcSpider(scrapy.Spider):
    name = 'src'
    allowed_domains = ['src.sjtu.edu.cn']
    start_urls = ['http://src.sjtu.edu.cn/list/?page=833']

    def parse(self, response):
        # print(u"[*]检查随机user-agnet", response.request.headers)

        html = response.text
        html_data = etree.HTML(html)

        item = ScarpyVulnsItem()
        for i in range(2, 17):
            item['time'] = html_data.xpath("//table/tr[%d]/td[1]/text()" % (i))[0]
            data2 = html_data.xpath("//table/tr[%d]/td[2]/a/text()" % (i))[0]
            tmp = data2.replace(' ', '')
            tmp = tmp.replace('\n', '')
            item['title'] = tmp
            item['rank'] = html_data.xpath("//table/tr[%d]/td[3]/span/text()" % (i))[0]
            item['author'] = html_data.xpath("//table/tr[%d]/td[4]/a/text()" % (i))[0]
            try:
                tmp = tmp.split(u"存在")
                item['organization'] = tmp[0]
                item['type'] = tmp[1]
            except:
                if u"大学" in tmp:
                    tmp = tmp.split(u"大学")
                    item['organization'] = tmp[0]+u"大学"
                    item['type'] = tmp[1]
                elif u"学院" in tmp:
                    tmp = tmp.split(u"学院")
                    item['organization'] = tmp[0]+u"学院"
                    item['type'] = tmp[1]
                else:
                    item['organization'] = tmp
                    item['type'] = "unknown"

            yield item

        # 获取分页的url
        nextpage = ''
        try:
            nextpage = html_data.xpath('/html/body/div/div/div[1]/div/div/ul/li[last()]/a/@href')[0]
        except:
            self.crawler.engine.close_spider(self, u"[*]已爬取到最后一页，完成爬取")

        if nextpage is not None:
            url = 'http://src.sjtu.edu.cn/list/%s' % (nextpage)
            yield Request(url=url,callback=self.parse)