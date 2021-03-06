#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-

from rent_house.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da86276486901629a048d1d0e06';

#主帐号Token
accountToken= '74c3d4fc131749bb95d341ccc6e06ac2';

#应用Id
appId='8a216da86276486901629a048d6e0e0c';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id


class CCP(object):
    '''自定义单例类，用于发送短信'''

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)


            # 初始化REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)

        return cls._instance


    def send_template_sms(self, to, datas, tempId):
        '''真正发送短信的方法
        返回值：如果是1，表示云通讯向我们发送短信是成功的，如果是0，表示失败'''

        # result: 是云通讯告诉开发者的结果信息
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # return的结果值，是开发者告诉用户短信是否发送成功
        if result.get('statusCode') == '000000':
            return 1
        else:
            return 0

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
    

# 参数1：目标手机
# 参数2：第一个元素：短信验证码 第二个元素：短信验证码的有效期 单位为分钟
# 参数3：短信的模板，默认提供的模板的id为1
# sendTemplateSMS('13113842566',['666666', '5'],1)