#!/usr/lib/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import time
import json

def send_request():
    base_url = 'http://fanyi.qq.com/api/translate'
    form_data = {
            'source':'auto',
            'target':'auto',
            'sourceText': raw_input('请输入需要翻译的文字：'),
            # 反爬点1：Unix时间戳生成表单数据
            "sessionUuid": "translate_uuid" + str(int(time.time() * 1000))
            #'sessionUuid': 'translate_uuid'+ str(int(time.time() * 1000))
        }
    data = urllib.urlencode(form_data)

    # 经多次试验,该请求报头会对 Cookie,Origin进行验证
    headers = {
                #"Accept": "application/json, text/javascript, */*; q=0.01",
                # "Accept-Encoding" : "gzip, deflate",
                #"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            
                #"Connection": "keep-alive",
                # "Content-Length" : "145",
                #"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": "pgv_pvi=718218240; RK=kO8/hNauMo; ptcz=8a6aa2eb109c92d6aa94aa7cc0aece1190b73987b80cc71037c056b024920137; pt2gguin=o0123636274; tvfe_boss_uuid=f21d3a8294e89358; mobileUV=1_15f9f25154c_a6c21; pgv_pvid=1030544080; o_cookie=123636274; pac_uid=1_123636274; fy_guid=9b09602e-d2ed-4797-930d-a8054582a349; ts_uid=5628386130; qtv=1b920999530fc4fd; qtk=x+ddTW4WjZSWiOjGDeB35xw+NZOqA22bM4aj1+RiDQ1yj+89CXrMZnIXHnCv00nta/HdipZn6CdyVEFYNSkcfG/lmmPd/W61Z6Zp4NmnXuseL04V8e1S5xdB/39tdIuvz8CMOpxEOfuGIN4z3Hcz+w==; pgv_info=ssid=s4651752224; ts_last=fanyi.qq.com/; openCount=1",
                #"Host": "fanyi.qq.com",
                "Origin": "http://fanyi.qq.com",
                #"Referer": "http://fanyi.qq.com/",
                #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                #"X-Requested-With": "XMLHttpRequest"
            }
    
    # 如果没有data参数， 就是get请求
    # 如果有data参数，就是一个post请求
    request = urllib2.Request(base_url, data, headers)
    request.add_header('Content-Length', len(data))

    print request.get_header('Content-length')
    response = urllib2.urlopen(request)
    return response.read()

if __name__ == '__main__':
    html = send_request()
    # 将一个json格式的字符串，转为对应的python数据类型
    dict_obj = json.loads(html)

    print(dict_obj['translate']['records'][0]['targetText'])


        








