# -*- coding: utf-8 -*-
import scrapy
from xici.items import XiciItem
from bs4 import BeautifulSoup
#from scrapy_redis.spiders import RedisSpider

class XiciSpider(scrapy.Spider):
#class XiciSpider(RedisSpider):
    name = 'weixin'
    start_urls = ['http://weixin.sogou.com/weixin?type=1&query=mycaijing&ie=utf8&_sug_=n&_sug_type_=']
    meta = {'how': 'ok'}
    first_url = ''
    redis_key = 'weixin:start_urls'

    def parse(self, response):
        sel = scrapy.Selector(response)
        #print(sel.xpath('//title').extract())
        fligint_div = "//ul[@class='news-list2']/li[1]/div[@class='gzh-box2']/div[@class='img-box']/a[1]/@href"
        first_url_list = sel.xpath(fligint_div).extract()
        self.first_url = first_url_list[0]
        print(self.first_url)
        yield  scrapy.Request(self.first_url,meta=self.meta, callback=self.parse_url_list)

    def parse_url_list(self,response):
        sel = scrapy.Selector(response)
        wait_text = sel.xpath("//p[@id='loading']//text()").extract()
        if wait_text:
            #验证码
            meta = response.meta
            meta['isscreen'] = 1
            #scrapy 有默认URL排重，不能有重复的url去请求
            yield scrapy.Request(response.url, meta=meta, callback=self.parse_validate,dont_filter=True)
        else:
            #正常分析html采集
            url_list = sel.xpath("//h4[@class='weui_media_title']/@hrefs").extract()
            for li in url_list:
                href = li.strip()
                url = 'http://mp.weixin.qq.com%s' % href
                #print(url)
                yield scrapy.Request(url, meta=self.meta, callback=self.parse_item)


    def parse_validate(self,response):
        print(response.xpath('//body').extract())
        yield scrapy.Request(self.first_url, meta=self.meta, callback=self.parse_url_list,dont_filter=True)


    def parse_item(self,response):
        result = XiciItem()
        url = response.url
        soup = BeautifulSoup(response.body,'lxml')
        title = soup.find('h2',id="activity-name").string
        content = soup.find('div',id="js_content").text
        #print(content)
        print(type(content))
        #exit()
        result['url'] = url
        result['title'] = title.strip()
        result['content'] = content
        yield result


