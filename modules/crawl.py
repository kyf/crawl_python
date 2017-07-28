#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import url
import ua
import time
import log
from random import *
from pyquery.pyquery import PyQuery 


class Crawl:

    #要访问的uri对象
    uri = None

    #访问间隔
    interval = []

    #访问时段
    tzone = []

    #是否访问下一级
    recursive = False    
    
    #请求头
    headers = {}

    
    #运行状态
    status = False


    def __init__(self, access_time, access_interval, target, recursive):
        if target.strip() == '':
            log.Errorf('请求的url不能为空')

        self.uri = url.parse(target)
        if self.uri is None:
            log.Errorf('请求的url格式错误', target)

        self.interval = access_interval
        self.tzone = access_time
        self.recursive = recursive

    
    def makeHeaders(self):
        return self.headers
            

    def run(self): 
        self.status = True
        log.Infof('crawl start running ...')
        while(True):
            if self.status == False:
                break
            self.request(str(self.uri), False)

    def pickSubUri(self, body):
        doc = PyQuery(body)
        result = []
        doc('a').each(lambda index, it : result.append(PyQuery(it).attr('href')))
        return result

    def request(self, target, isSub):        
        if target in ('/'):
            return
        item = url.parse(target)
        if item.scheme == '':
            item.scheme = self.uri.scheme

        if item.host == '':
            item.host, item.port = self.uri.host, self.uri.port

        target = item

        if target.scheme not in ('http', 'https'):
            return

        hour = time.strftime('%H')
        if hour not in self.tzone and len(self.tzone) > 0:
            time.sleep(10)
            return

        userAgent = ua.rand()
        headers = self.makeHeaders()
        headers['User-Agent'] = userAgent
        log.Infof('%s ...', str(target))
        resp = requests.get(target, headers = self.headers, verify = False)
        if resp.status_code != 200:
            log.Infof('请求失败，响应状态码：%d', resp.status_code)
         
        resp.encoding = 'utf-8'
        if self.recursive and isSub == False:
            subUris = self.pickSubUri(resp.text)
            for it in subUris:
                if not self.status:
                    return
                self.request(it, True)

        time.sleep(choice(range(int(self.interval[0]), int(self.interval[1]))))

    def stop(self):
        self.status = False
        log.Infof('crawl will be exit!')
    


