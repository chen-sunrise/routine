# -*- coding:utf-8 -*-


import urllib2
import urllib
import cookielib


def login():
    '''登录模块，产生保存Cookie的opener对象'''
    # 1.创建保存Cookie的cookiejar对象
    cookie_jar = cookielib.CookieJar()
    # 2. 使用Cookiejar对象，构建handle处理器
    cookie_handle = urllib2.HTTPCookieProcessor(cookie_jar)
    # 3.再通过handle处理器，构建自定义opener对象
    opener = urllib2.build_opener(cookie_handle)

    login_url = 'http://www.renren.com/PLogin.do'
    form_data = {"email" : "mr_mao_hacker@163.com", "password" : "alarmchime"}
    data = urllib.urlencode(form_data)
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    request = urllib2.Request(login_url, data, headers)

    # 发送登录的post请求，登录成功则自动保存Cookie
    opener.open(request)

    # 1.返回opener对象，传递给其他函数使用
    # return opener
    # 2.通过install_opener将自定义opener加载为全局权限，这样在代码的任何地方使用urlopen()都具有opener的功能
    urllib2.install_opener(opener)


def main():
    '''通过opener对象处理并传递Cookie，获取需要登录权限的页面数据'''

    # 如果login()是return的话，则接收opener对象
    login()

    url_list = [
        "http://www.renren.com/327550029/profile",
        "http://www.renren.com/410043129/profile"
    ]

    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    for index, url in enumerate(url_list):
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request).read()

        with open('renren_' + str(index) + '.html', 'w') as f:
            f.write(response)


if __name__ == '__main__':
    main()



