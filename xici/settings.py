# -*- coding: utf-8 -*-

# Scrapy settings for xici project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xici'

SPIDER_MODULES = ['xici.spiders']
NEWSPIDER_MODULE = 'xici.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xici (+http://www.yourdomain.com)'

# Obey robots.txt rules


ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True

#scrapy-proxy 代理（代理池管理），从数据库控制代理；不符合的代理IP（超过重复次数，和使用时间）计划任务定期清洗
# RETRY_ENABLED = True
# RETRY_TIMES = 10
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408,521]
DOWNLOADER_MIDDLEWARES = {
    #'xici.middlewares.myRetryMiddleware': 100,#错误重新采集机制，用来管理代理IP池，如果代理IP超过3次就从数据库删除
    #'xici.middlewares.myRandomProxy': 200,#从数据库中读取有效的代理IP，做代理池
    'xici.middlewares.XiciSpiderMiddleware' :400,#phantomjs模拟浏览器返回response
    #'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,

}
#PROXY_MODE = 0


#scrapy-redis 分布式,不同机器运行相同采集任务，会爬不同链接，增加其采集效率
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# REDIS_HOST = '192.168.31.22'
# REDIS_PORT = 6379

DOWNLOAD_DELAY = 1


ITEM_PIPELINES = {
   #'xici.pipelines.XiciPipeline': 300,
   'xici.pipelines.MongoPipeline': 300,
   #'scrapy_redis.pipelines.RedisPipeline': 400,
}
LOG_LEVEL = 'INFO'


#打码平台配置
VALIDATE = {
    'username':'',
    'password':'',
    'soft_id':'',
    'soft_key':'',
}

