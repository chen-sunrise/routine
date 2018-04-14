#!/urs/lib/env pyhton
# -*- coding:utf-8 -*-

import urllib
import urllib2


def send_request(url):
    '''
        发送请求，返回响应
        url:需要发送请求的url地址
        return 返回响应页面的字符串
    '''
    
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    
    request = urllib2.Request(url, headers = headers)
    try:
        response = urllib2.urlopen(request)
        return response.read()
    except Exception as e:
        print(e)
        return ''

def write_page(html, filename):
    '''
        写入相应字符串到磁盘文件中
        html: 响应字符串
        filename:磁盘文件的文件名
    '''
    print '[INFO] 正在写入文件' + filename
    with open(filename, 'w') as f:
        f.write(html)


def main(tieba_name, begin_page, end_page):
    '''
        贴吧调度器，构建url地址，并传递发送
        tieba_name:贴吧名
        begin_page:起始页
        end_page:结束页
    '''

    for page in range(begin_page, end_page + 1):

        # 处理url地址和查询字符串
        base_url = 'http://tieba.baidu.com/f?'
        pn = (page - 1) * 50
        query_data = {'kw': tieba_name, 'pn' : pn}
        # 将query_data转为16进制数
        query_str = urllib.urlencode(query_data)
        print query_str
        full_url = base_url + query_str

        filename = tieba_name + str(page) + '.html'
        html = send_request(full_url)
        write_page(html, filename)



if __name__ == "__main__":
    tieba_name = raw_input('请输入需要爬取的贴吧名：')
    begin_page = int(raw_input('请输入需要爬取的起始页：'))
    end_page = int(raw_input('请输入需要爬取的结束页：'))
    main(tieba_name, begin_page, end_page)
