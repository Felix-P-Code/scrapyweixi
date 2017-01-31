#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice
import time
import os
from xici.settings import *
from PIL import Image
from xici.common.rcclient import RClient


def selenium_request(url ,isscreen = False):
    osurl = '%s/xici/validateimg/' % os.path.dirname(os.path.abspath("scrapy.cfg"))

    ua_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
    ]

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.resourceTimeout"] = 15
    dcap["phantomjs.page.settings.loadImages"] = True
    dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)
    driver = webdriver.PhantomJS(executable_path='/Users/felixchan/Tool/phantomjs',desired_capabilities=dcap)
    # driver = webdriver.Firefox()
    driver.get(url)
    if isscreen:
        imgURL = '%s%s.png' % (osurl,int(time.time()))
        uploadimg = '%s%s_2.png' % (osurl,int(time.time()))
        driver.save_screenshot(imgURL)  # 截图保存
        time.sleep(1)

        ocr = RClient(VALIDATE['username'], VALIDATE['password'], VALIDATE['soft_id'], VALIDATE['soft_key'])
        left = 260
        top = 12
        right = 396
        bottom = 70

        im = Image.open(imgURL)
        im = im.crop((left, top, right, bottom))
        im.save(uploadimg)
        ims = open(uploadimg, 'rb').read()
        post_result = ocr.create(uploadimg,ims, 3040)
        varidate_code = post_result['Result']
        print(post_result)


        elem = driver.find_element_by_id('input')
        elem.send_keys(varidate_code)
        #elem.send_keys(Keys.ENTER)  #点击键盘上的Enter按钮
        driver.find_element_by_id('bt').click()  # 点击了百度页面上的‘百度一下’按钮
        #driver.refresh()

    driver.implicitly_wait(2)
    time.sleep(1)
    true_page = driver.page_source  # .decode('utf-8','ignore')
    driver.close()
    return true_page







