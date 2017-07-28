#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getopt import getopt
import sys
from modules.crawl import Crawl 
import signal


VERSION = '0.0.1'
AUTHOR  = 'kyf10086'
DATE    = '2017-07-28'

craw = None


def usage():
    note = '''
Usage:
    main.py [options]

    Options:
       -H, --host              请求访问的主地址url，如http://www.baidu.com
       -r, --recursive=0       是否访问下一级，默认为0(不访问)，否则设置为1
       -i, --interval          请求的间隔区间，最小秒数和最大秒数, 默认为5,10.  如3,5.  (注意是英文逗号分割)
       -t, --time              请求时段，如果不设定，默认是所有时段.如1,5,9,12  
       -h, --help              打印帮助文档
       -v, --version           查看当前版本
'''

    print note

def showVersion():
    print '简单爬虫工具 version %s, build %s, %s' % (VERSION, AUTHOR, DATE)


def handleSignal(signum, stack):
    if crawl is not None:
        crawl.stop()


def main(argv):
    options, _ = getopt(argv, 'hvi:t:H:r:', ['help', 'version', 'interval=', 'time=', 'host=', 'recursive='])
    if len(options) == 0:
        usage()
        return

    access_time = []
    access_interval = [5, 10]
    host = ''
    recursive = False
    for (k, v) in options:
        k = k.strip('-')
        if k in ('h', 'help'):
            usage()
            return
        if k in ('v', 'version'):
            showVersion()
            return
        if k in ('t', 'time'):
            access_time = v.split(',')
        if k in ('i', 'interval'):
            access_interval = v.split(',')
        if k in ('H', 'host'):
            host = v
        if k in ('r', 'recursive'):
            if v == '1':
                recursive = True
            else: 
                recursive = False

    signal.signal(signal.SIGINT, handleSignal)

    global crawl
    crawl = Crawl(access_time, access_interval, host, recursive)
    crawl.run()

if __name__ == '__main__':
    main(sys.argv[1:])
