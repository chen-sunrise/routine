import requests
from lxml import etree
from queue import Queue
# from multiprocessing.dummy import Pool
import threading
import time

class DoubanSpider(object):
    def __init__(self):
        self.start_urls = ["https://movie.douban.com/top250?start=" + str(page) for page in range(0, 226, 25)]
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.data_queue = Queue()
        self.proxy = {"http" : "http://maozhaojun:ntkn0npx@114.67.224.167:16819"}
        # self.proxy = []
        self.count = 0

    def send_request(self,url):
        try:
            print ("[INFO]: 正在抓取 %s" % url)
            response = requests.get(url, headers = self.headers, proxies = self.proxy)
            time.sleep(1)
            # print(response)
            self.parse_page(response)
        except Exception as e:
            print('[ERROR] %s 请求发送失败' % self.start_urls)
            print(e)

    def parse_page(self, response):
        html_obj = etree.HTML(response.content)
        # //div[@class='info']/div[@class='bd']/div[@class='star']/span[2]/text()
        node_list = html_obj.xpath("//div[@class='info']")
        for node in node_list:
            title = node.xpath(".//div[@class='hd']/a/span[1]/text()")
            score = node.xpath(".//span[@class='rating_num']/text()")[0]
            try:
                info = node.xpath(".//span[@class='inq']/text()")[0]
            except:
                info = 'None'
            # print(str(title) + '\t' + str(score)+ '\t' + str(info))
            self.count += 1
            self.data_queue.put(str(title) + "\t" + str(score) + "\t" + str(info))
            # with open('douban.txt', 'w') as f:
            #     f.write(data)

    def main(self):
        thread_list = []
        for url in self.start_urls:
            thread = threading.Thread(target=self.send_request, args= [url])
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()
        while not self.data_queue.empty():
            print(self.data_queue.get())
        print(self.count)


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main()
