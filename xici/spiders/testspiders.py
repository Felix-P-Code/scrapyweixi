import scrapy
from xici.items import ProxyItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com',
    )
    meta = {'how': 'ok'}

    '''
    改为客户配置:scrapy配置等级default > project > custom
    '''
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'xici.middlewares.myRandomProxy': None,  # 从数据库读取可用代理IP
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'xici.middlewares.XiciSpiderMiddleware': 400,  # phantomjs模拟浏览器返回response
        },
        'ITEM_PIPELINES': {
            # 'xici.pipelines.XiciPipeline': 300,
            'xici.pipelines.ProxyPipeline': 300,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
        },
        'SCHEDULER':'scrapy.core.scheduler.Scheduler',
        'DUPEFILTER_CLASS':'scrapy.dupefilters.RFPDupeFilter',
        'SCHEDULER_PERSIST':None,
        'SCHEDULER_QUEUE_CLASS':None
    }

    # print(scrapy.settings.default_settings)

    def start_requests(self):
        '''需爬取的链接'''
        reqs = []

        for i in range(1, 2):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s" % i,meta=self.meta)
            reqs.append(req)

        return reqs

    def parse(self, response):
        #打印全局的默认配置
        #print("Existing settings: %s" % self.settings.attributes.keys())

        trs = response.xpath('//table[@id="ip_list"]/tbody/tr')
        item = ProxyItem()
        for tr in trs[1:]:
            item['ip'] = tr.xpath('td[2]/text()')[0].extract()
            item['port'] = tr.xpath('td[3]/text()')[0].extract()
            item['position'] = tr.xpath('string(td[4])')[0].extract().strip()
            item['http_type'] = tr.xpath('td[6]/text()')[0].extract()
            item['speed'] = tr.xpath('td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['connect_time'] = tr.xpath('td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            item['check_time'] = tr.xpath('td[10]/text()')[0].extract()
            item['error_time'] = 0
            yield  item
