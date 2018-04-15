#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import random
import hashlib
import json
import urllib
import urllib2

def send_request():

    # js解密算法数据
    r = str(int(time.time() * 1000) + random.randint(0, 10))
    D = "ebSeFb%=XZ%T[KZ)c(sy!"
    S = "fanyideskweb"
    n = raw_input("请输入需要翻译的文字:")
    sign = hashlib.md5(S + n + r + D).hexdigest()

    form_data = {
        "i" : n,
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

    base_url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    headers = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        #"Accept-Encoding" : "gzip, deflate",
        "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection" : "keep-alive",
        "Content-Length" : "218",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie" : "_ntes_nnid=f77d53cb936304b5333b304b767a4958,1506087321856; OUTFOX_SEARCH_USER_ID_NCOO=971893961.4325761; OUTFOX_SEARCH_USER_ID=-1480774266@10.169.0.83; JSESSIONID=aaaouUJJcJbTucFMz-8kw; ___rl__test__cookies=1523590284588",
        "Host" : "fanyi.youdao.com",
        "Origin" : "http://fanyi.youdao.com",
        "Referer" : "http://fanyi.youdao.com/",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "X-Requested-With" : "XMLHttpRequest"
    }

    request = urllib2.Request(base_url, data, headers)

    request.add_header("Content-Length", len(data))
    response = urllib2.urlopen(request)
    return response.read()

if __name__ == "__main__":
    html = send_request()
    dict_obj = json.loads(html)
    print dict_obj["translateResult"][0][0]["tgt"]


