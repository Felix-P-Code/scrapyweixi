# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse
from scrapy_proxies.randomproxy import RandomProxy
from xici.common.func import selenium_request
from pymongo import MongoClient
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class XiciSpiderMiddleware(object):

    def process_request(self, request, spider):

        if 'how' in request.meta:

            if 'isscreen' in request.meta:
                print(1)
                true_page = selenium_request(request.url,True)
            else:
                true_page = selenium_request(request.url)

            return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request, )


class myRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            #print(dir(response))
            #print(''.join(['%s:%s' % item for item in response.__dict__.items()]))
            if 'proxy' in request.meta:
                ip = request.meta['proxy'].replace('http://', '')
                iplist = ip.split(':')
                ip = iplist[0]
                conn = MongoClient('localhost', 27017)

                db = conn.scrapy  # 连接数据库
                result = db.proxy.find_one({'ip': ip})
                error_time = result['error_time'] + 1
                db.proxy.update({'ip': ip}, {"$set": {"error_time": error_time}})

                if error_time == 3:
                    db.proxy.remove({'ip': ip})

            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response



class myRandomProxy(RandomProxy):

    def __init__(self, settings):
        # self.proxy_list = settings.get('PROXY_LIST')
        #
        # if self.proxy_list is None:
        #     raise KeyError('PROXY_LIST setting is missing')
        #
        # fin = open(self.proxy_list)
        #
        # self.proxies = {}
        # for line in fin.readlines():
        #     parts = re.match('(\w+://)(\w+:\w+@)?(.+)', line.strip())
        #     if not parts:
        #         continue
        #
        #     # Cut trailing @
        #     if parts.group(2):
        #         user_pass = parts.group(2)[:-1]
        #     else:
        #         user_pass = ''
        #
        #     self.proxies[parts.group(1) + parts.group(3)] = user_pass
        #
        # fin.close()
        conn = MongoClient('localhost', 27017)
        db = conn.scrapy  # 连接数据库
        items = {}
        for item in db.proxy.find({"error_time": {'$gte': 0, '$lt': 4}}):
            key = 'http://%s:%s' % (item['ip'], item['port'])
            items[key] = ''

        self.proxies = items
