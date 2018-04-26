# -*- coding:utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup
import time


class SpiderTencent(object):
    def __init__(self):
        self.start_url = "https://hr.tencent.com/position.php?&start=0"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
        self.item_list = []
        self.page = 0

    def send_request(self, url):
        response = requests.get(url, headers = self.headers)
        return response

    def parse_page(self, response):
        html = response.content
        print response.status_code
        # print html
        soup = BeautifulSoup(html, 'lxml')
        # 获取十个职位的节点列表
        node_list = soup.select('.even, .odd')
        for node in node_list:
            item = {}
            item["position_name"] = node.select("td a")[0].get_text()
            item["position_link"] = node.select("td a")[0].get("href")
            item["position_type"] = node.select("td")[1].get_text()
            item["position_number"] = node.select("td")[2].get_text()
            item["work_local"] = node.select("td")[3].get_text()
            item["publish_times"] = node.select("td")[4].get_text()
            self.item_list.append(item)
        if soup.find('a', {'class':'noactive', 'id':'next'}):
            return None
        else:
            next_link = 'https://hr.tencent.com/' + soup.find('a', {'id':'next'}).get('href')
            return next_link

    def write_info(self):
        json.dump(self.item_list, open('tencent.json', 'w'))

    def main(self):
        response = self.send_request(self.start_url)
        # print response
        while self.page < 50:
            next_link = self.parse_page(response)
            # print next_link
            if next_link is None:
                print '到了最后一页'
                break
            else:
                try:
                    response = self.send_request(next_link)
                    # print response
                except:
                    print "[Error] 请求处理失败.." + next_link
            self.page += 1
            print '第%s页爬取成功' % self.page
        self.write_info()


if __name__ == '__main__':
    spider = SpiderTencent()
    spider.main()