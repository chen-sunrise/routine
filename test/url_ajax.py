# !/usr/lib/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2


def send_request():
    base_url = 'https://movie.douban.com/j/chart/top_list?'
    #for start in range(1,8) * 20:
    query_data = {
            'type':'11',
            'interval_id':'100:90',
            'action':'',
            'start':'20',
            'limit':'20'
        }
    
    query_str = urllib.urlencode(query_data)
    full_url = base_url + query_str

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(full_url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()

    return html

if __name__ == '__main__':
    html = send_request()
    filename = '豆瓣' + '.html'
    with open(filename, 'w') as f:
        f.write(html)


