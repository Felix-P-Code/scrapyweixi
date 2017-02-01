# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse

from xici.common.func import selenium_request


class XiciSpiderMiddleware(object):

    def process_request(self, request, spider):
        # flag = False
        # #print(request.meta.has_key('isscreen'))
        # for d, v in en umerate(request.meta):
        #     if v == 'how':
        #         print(d,'---',v)
        #         flag = True
        #         break


        if 'how' in request.meta:

            if 'isscreen' in request.meta:
                print(1)
                true_page = selenium_request(request.url,True)
            else:
                true_page = selenium_request(request.url)

            return HtmlResponse(request.url, body=true_page, encoding='utf-8', request=request, )

