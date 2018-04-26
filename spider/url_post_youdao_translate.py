#!/usr/lib/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import json
import time
import hashlib
import random


def send_request():
    
    base_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

    # js解密算法数据
    r = str(int(time.time() * 1000) + random.randint(0,10))
    n = raw_input('请输入需要翻译的文字：')
    S = "fanyideskweb"
    D = "ebSeFb%=XZ%T[KZ)c(sy!"

    sign = hashlib.md5(S + n + r + D).hexdigest()

    form_data = {"i" : n,
            "from" : "AUTO",
            "to" : "AUTO",
            "smartresult" : "dict",
            "client" : "fanyideskweb",
            "salt" : r,
            "sign" : sign,
            "doctype" : "json",
            "version" : "2.1",
            "keyfrom" : "fanyi.web",
            "action" : "FY_BY_CLICKBUTTION",
            "typoResult" : "false"
        }
    
    data = urllib.urlencode(form_data)

    headers = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        #"Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "zh-CN,zh;q=0.8",
        "Connection" : "keep-alive",
        #"Content-Length" : "41",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie" : "OUTFOX_SEARCH_USER_ID=964333011@183.235.255.52; JSESSIONID=aaaDp1__ltTNq7qRDg-kw; OUTFOX_SEARCH_USER_ID_NCOO=958705096.4572818; ___rl__test__cookies=1523625329420",
        "Host" : "fanyi.youdao.com",
        "Origin" : "http//fanyi.youdao.com",
        "Referer" : "http//fanyi.youdao.com/",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "X-Requested-With" : "XMLHttpRequest"
        }

    request = urllib2.Request(base_url, data, headers)
    request.add_header('Content-Length', len(data))
    response = urllib2.urlopen(request)
    html = response.read()
    return html


if __name__ == "__main__":
    html = send_request()
    dict_obj = json.loads(html)
    print dict_obj["translateResult"][0][0]["tgt"]
