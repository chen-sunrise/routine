#!/usr/lib/python2.7
# -*- coding:utf-8 -*-

import urllib
import urllib2

def send_request():
    base_url = "http://www.baidu.com/s?"
    keyword = raw_input("请输入需要查询的关键字：")
    
    # 将字典转换成为url编码的字符串
    url_str = urllib.urlencode({'wd': keyword, 'ie': 'utf-8'})
    # 在和固定url地址部分进行拼接
    full_url = base_url + url_str
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    # 构造请求，发送
    request = urllib2.Request(full_url, headers = headers)

    response = urllib2.urlopen(request)
    return response.read()

if __name__ == "__main__":
    html = send_request()
    print html

    

