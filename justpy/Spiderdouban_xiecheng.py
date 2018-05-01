import requests
import pickle
import sys
from lxml import etree
from queue import Queue
import time
import gevent
from gevent import monkey
# 猴子补丁：将python底层的网络库socket selecth打个补丁，这些网络库模块在处理网络IO时会按异步的方式处理
monkey.patch_all()


class SpiderDouban(object):
    def __init__(self):
        self.start_urls = ["https://movie.douban.com/top250?start=" + str(page) for page in range(0, 226, 25)]
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.count = 0
        self.data_queue = Queue()
        self.proxy = {"http": "http://maozhaojun:ntkn0npx@114.67.224.167:16819"}

    def send_request(self, url):
        response = requests.get(url, headers =self.headers, proxies = self.proxy)
        time.sleep(1)
        self.parse_page(response)

    def parse_page(self, response):
        html_obj = etree.HTML(response.content)
        # 取每一个电影结点
        node_list =  html_obj.xpath('//div[@class="info"]')
        for node in node_list:
            title = node.xpath(".//div[@class='hd']/a/span[1]/text()")[0]
            score = node.xpath(".//span[@class='rating_num']/text()")[0]
            try:
                info = node.xpath(".//span[@class='inq']/text()")[0]
            except:
                info = 'None'
            self.count += 1
            self.data_queue.put(title + "\t" + score + "\t" + info)


    def main(self):
        '''
        for url in self.start_urls:
            self.send_request(url)
        :return: 
        '''
        spawn_list = []
        for url in self.start_urls:
            job = gevent.spawn(self.send_request, url)
            spawn_list.append(job)
        gevent.joinall(spawn_list)

        # gevent.joinall([gevent.spawn(self.send_request, url)])

        # 判断对列为空时，循环取值结束
        while not self.data_queue.empty():
            data = self.data_queue.get()
            # print(type(data))
            # with open('douban.txt', 'w') as f:
            #     f.write(data)
        print(self.count)
        print(sys.getdefaultencoding())


if __name__ == '__main__':
    spider = SpiderDouban()
    start = time.time()
    spider.main()
    print('执行的时间为 %f' % (time.time() - start))