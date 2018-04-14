#!usr/lib/env python
# -*- coding:utf-8 -*-

import urllib2

def send_request():
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    url = 'http://www.baidu.com'

    # 构建一个HTTPHandler处理器对象，支持处理HTTP请求
    #http_handler = urllib2.HTTPHandler()
    
    # 调用urllib2.bulid_opener()方法，创建支持处理HTTP请求的opener对象
    #opener = urllib2.build_opener(http_handler)
    
    #request = urllib2.Request(url, headers = headers)
    #print(request.get_header('User-agent'))
    #response = opener.open(request)
    
    response =  urllib2.urlopen(urllib2.Request(url, headers = headers)).read()
    return response


def send_request1():
    url = 'http://www.itcast.cn'
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(url, headers = headers)
    http_handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(http_handler)
    response = opener.open(request)
    return response.read()

if __name__ == '__main__':
    html = send_request1()
    print html

