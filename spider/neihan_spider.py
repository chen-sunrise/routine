# -*- coding:utf-8 -*-


import requests
import re
import sys


class NeihanSpider(object):
    def __init__(self):
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.base_url = "http://www.neihanpa.com/article/list_5_"
        self.page = 1
        self.pattern_page = re.compile('<div class="f18 mb20">(.*?)</div>', re.S)
        # self.pattern_page = re.compile('<div class="f18 mb20">(.*?)</div>', re.S)

        # self.pattern_result = re.compile("<.*?>|&.*?;|\s|　")
        # 用来处理无用字符
        # <.*?> 表示标签
        # &.*?; 表示匹配HTML实体字符
        # \s 表示匹配空白字符
        # u"\u3000".encode("utf-8") 表示匹配全角中文空格
        self.parrent_result = re.compile('<.*?>|&.*?;|\s|' + u'\u3000'.encode('utf-8'))

    def send_request(self, url):
        proxy = {"http" : "http://maozhaojun:ntkn0npx@114.67.224.167:16819"}
        # 后面加了.content返回的是字节流数据
        html = requests.get(url, headers = self.headers, proxies=proxy).content
        html = html.decode('gbk').encode('utf-8')

        return html

    def parse_page(self, html):
        # 提取所有段子内容，返回列表
        result_list = self.pattern_page.findall(html)
        return result_list

    def write_page(self, result_list):
        with open('duanzi.html', 'a') as f:
            f.write('第'+ str(self.page) + '页:\n')
            # print result_list
            for result in result_list:
                content = self.parrent_result.sub('',result)
                f.write(content + '\n')
                # f.write("\n")
            f.write('\r\n')

    def main(self):
        while True:
            # if self.page == 5:
            #     break
            full_url = self.base_url + str(self.page) + '.html'
            try:
                html = self.send_request(full_url)
                # print html
                result_list = self.parse_page(html)
                # print result_list
                self.write_page(result_list)
                self.page += 1
            except Exception as e:
                print e

            comment = raw_input('按回车继续爬取（退出输入q）:')
            if comment == 'q':
                break
        # while True:
        #     full_url = self.base_url + str(self.page) + ".html"
        #     try:
        #         html = self.send_request(full_url)
        #         result_list = self.parse_page(html)
        #         self.write_page(result_list)
        #         self.page += 1
        #     except Exception as e:
        #         print e
        #         print "[ERROR]: 页面抓取失败" + full_url
        #
        #     command = raw_input("按回车继续爬取（退出输入q）:")
        #     if command == 'q':
        #         print "[INFO] 谢谢使用，再见!"
        #         break


if __name__ == '__main__':
    spider = NeihanSpider()
    spider.main()


