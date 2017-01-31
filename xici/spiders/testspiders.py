# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from xici.items import XiciItem


class TestSpider(scrapy.Spider):
    name = 'weixin2'
    #start_urls = ['http://epaper.21jingji.com/html/2017-01/23/node_1.htm']

    def start_requests(self):
        meta = {'how': 'ok'}
        link = 'http://epaper.21jingji.com/html/2017-01/23/node_1.htm'
        yield scrapy.Request(link, meta=meta,callback=self.parse_url_list)


    def parse_url_list(self,response):
        url_list = response.xpath("//div[@class='news_list']/ul/li/a/@href").extract()
        print(url_list)
        items = []
        meta = {'how': 'ok'}
        i = 0
        for url in url_list:
            if i<5:
                #++i
                i = i+1
                href = 'http://epaper.21jingji.com/html/2017-01/23/%s' % url
                yield scrapy.Request(href,meta=meta, callback=self.parse_url_itme)
            else:
                break


    def parse_url_itme(self,response):
        result = XiciItem()
        #result = {}
        #body = selenium_request(href)
        #print(response.body)
        soup = BeautifulSoup(response.body, "lxml")
        title_tag = soup.find_all("h1")
        title = title_tag[1].text.strip()
        if title:
            result['url'] = response.url
            result['title'] = title
            print(response.url,title_tag)
            yield result



    def parse_scrapy(self, response):
        url_list = response.xpath("//div[@class='news_list']/ul/li/a/@href").extract()
        items = []
        for url in url_list:
            href = 'http://epaper.21jingji.com/html/2017-01/23/%s' % url
            yield scrapy.Request(href, callback=self.parse_scrapy_item)



    def parse_scrapy_item(self, response):
        result = XiciItem()
        url  =  response.url
        title = response.xpath('//h1[2]//text()').extract()
        result['url'] = url
        result['title'] = title[0]
        yield result