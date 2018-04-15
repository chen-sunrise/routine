#!/usr/lib/env python
# -*- coding:utf-8 -*-


import urllib2

def send_request():
    url = 'http://192.168.72.82/'
    # web验证的账户
    username = "bigcat"
    # web验证的密码
    password = "123456"
    # 构建一个基于HTTP验证的处理器对象
    passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # 添加web信息和账户密码
    passmgr.add_password(None,url,username,password)
    # 构建处理器对象
    httpauth_handle = urllib2.HTTPBasicAuthHandler(passmgr)
    opener = urllib2.build_opener(httpauth_handle)
    response = opener.open(url)

    return response.read()

if __name__ == '__main__':
    send_request()