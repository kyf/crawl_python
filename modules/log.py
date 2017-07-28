#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import strftime
import os

def Errorf(fmt, *args):
    prefix = '[ERROR]'
    log(fmt, prefix, args)
    os._exit(1)


def Infof(fmt, *args):
    prefix = '[INFO]'
    log(fmt, prefix, args)


def log(fmt, prefix, args):    
    now = '[%s]' % strftime('%Y-%m-%d %H:%M:%S')
    fmt = now + fmt
    print fmt % args



