# -*- coding:utf-8 -*-

import requests
from lxml import etree

def send_request():
    url = 'https://uact.douyucdn.cn/uact.do'
    headers = {"Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Connection": "keep-alive",
               "Content-Length": "811",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Host": "uact.douyucdn.cn",
               "Origin": "https://www.douyu.com",
               "Referer": "https://www.douyu.com/directory/game/yz",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.3"
               }
    data = {"multi":[{"d":"ab68db3de4d4d463449af30100001501","i":0,"rid":0,"u":"/directory/game/yz","ru":"/directory","ac":"show_recommend_livelist_room","rpc":"page_classify","pc":"page_live","pt":1523878701914,"oct":1523878716680,"dur":0,"pro":"host_site","ct":"web","e":{"pos":9,"pg":1,"rid":"3755535","rt":"1801","tid":201,"rpos":0,"sub_rt":0,"chid":790,"cid":8,"s_name":"tag","name":"在线直播","is_all":1,"is_on":1,"rac":"show_recommend_livelist_room"},"av":"","up":""}],
"v":1.5}
    response = requests.post(url, headers =headers,data=data)
    print response.content

    # html = response.json()
    #
    # html_obj = etree.JSON(html)
    # link_list = html_obj.xpath('//img[@class=JS_listthumb]/@src')
    # for link in link_list:
    #     response = requests.get(link, headers=headers)
    #     with open(link[-15:], 'w') as f:
    #         f.write(response.content)


if __name__ == '__main__':
    send_request()